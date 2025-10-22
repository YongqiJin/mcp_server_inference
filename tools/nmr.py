import httpx
from httpx import Timeout
DEFAULT_TIMEOUT = Timeout(120.0, connect=300.0)

from structs.nmr import (
    SearchParam,
    PredictParam,
    ReversePredictParam,
    InputNMR,
    Result,
    TaskSubmit,
    transform_predict_param,
    transform_reverse_predict_param,
    transform_search_param
)
from structs.base import RES
from tools.chem_tools import draw_mol_with_nmr
from rdkit import Chem
# from loguru import logger
import tempfile
import time
from dp.agent.server.storage.bohrium_storage import BohriumStorage
from tools.env import BOHRIUM_PASSWORD, BOHRIUM_USERNAME, BOHRIUM_PROJECT_ID
import os

BOHRIUM_USERNAME = os.getenv("BOHRIUM_USERNAME")
BOHRIUM_PASSWORD = os.getenv("BOHRIUM_PASSWORD")
BOHRIUM_PROJECT_ID = os.getenv("BOHRIUM_PROJECT_ID")


def add_svg(res:Result)->Result:
    storage = BohriumStorage(username=BOHRIUM_USERNAME, password=BOHRIUM_PASSWORD, project_id=BOHRIUM_PROJECT_ID)
    """Upload svg to bohrium storage and add the link to the result
    """
    svg_content = draw_mol_with_nmr(
        mol_list=[Chem.MolFromSmiles(res.smiles_with_atom_order, sanitize=False)],
        shifts_list=[res.atoms_shift],
        nmr_type=['H', 'C'],
        size=(300, 300),
        fontscale=0.6,
    )
    try:
        timestamp = int(time.time())
        with tempfile.NamedTemporaryFile(delete=True, suffix=".svg") as f:
            f.write(svg_content.encode("utf-8"))
            key = storage.upload(
                f"nmr_svg/{timestamp}/",
                f.name,
            )
            # logger.info(f"upload svg to bohrium storage: {key}")
            http_url = storage.get_http_url(key)
            # logger.info(f"uploaded svg can be fetch with: {http_url}")
            res.svg = f"{http_url}"
    except Exception as e:
        # logger.error(f"upload svg to bohrium storage error: {e}")
        raise e
    
    return res
    
def transform_result(res:RES[list[Result]])->RES[list[Result]]:
    res.data = [add_svg(_res) for _res in res.data]
    return res

async def NMR_search(data:SearchParam)-> RES[list[Result]]:
    try:
        payload = TaskSubmit(input_data=transform_search_param(data))
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/sync_nmr_service_mcp"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw['data']['result'])
            res.msg = "success"  # avoid extra message from origin server
            res = transform_result(res)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr search error: {e}")


async def NMR_predict(data:PredictParam)->RES[list[Result]]:
    try:
        payload = TaskSubmit(input_data=transform_predict_param(data))
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/sync_nmr_service_mcp"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw['data']['result'])
            res = transform_result(res)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr predict error: {e}")


async def NMR_reverse_predict(data:ReversePredictParam) ->RES[list[Result]]:
    try:
        payload = TaskSubmit(input_data=transform_reverse_predict_param(data))
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            url = "http://101.126.67.113:8090/sync_nmr_service_mcp"

            payload = payload.model_dump(exclude_none=True)
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_raw = response.json()
            res = RES[list[Result]](**res_raw['data']['result'])
            res = transform_result(res)
            return res
    except Exception as e:
        return RES(code=-1, msg=f"nmr reverse_predict error: {e}")
