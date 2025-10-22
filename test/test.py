import sys, time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)

from tools.base import (
    ADMET_predict,
    Pharmacokinetics_predict,
    ToxScan_predict,
    InputData,
    InputPK,
    RES
)
from tools.nmr import NMR_search, NMR_predict,NMR_reverse_predict,SearchParam,PredictParam,ReversePredictParam,InputNMR,Result,TaskSubmit
import asyncio

class Demo:
    smiles = "Cc1ccccc1CC#CC(O)c1ccccc1C"
    h_shifts = [2.16, 2.29, 2.29, 2.29, 2.41, 2.41, 2.41, 3.58, 3.58, 5.63, 7.17, 7.17, 7.17, 7.17, 7.17, 7.17, 7.39, 7.64]
    c_shifts = [19.1, 19.4, 23.5, 62.7, 82.1, 84.5, 126.27, 126.3, 126.5, 127, 128.36, 128.41, 130.2, 130.8, 134.8, 135.98, 136.02, 138.9]
    allowed_elements = ['C', 'H', 'O', 'N']
    formula = "C18H18O"
    topk = 5

demo = Demo()


async def test():
    start = time.time()
    tasks = [
        NMR_search(SearchParam(C_shifts=demo.c_shifts, topk=demo.topk)),
        # NMR_search(SearchParam(H_shifts=demo.h_shifts, C_shifts=demo.c_shifts, allowed_elements=demo.allowed_elements)),
        # NMR_predict(PredictParam(smiles_list=[demo.smiles]*2)),
        # NMR_reverse_predict(ReversePredictParam(C_shifts=demo.c_shifts, topk=demo.topk)),
        # NMR_reverse_predict(ReversePredictParam(H_shifts=demo.h_shifts, C_shifts=demo.c_shifts, allowed_elements=demo.allowed_elements, formula=demo.formula)),
    ]
    # res_list:list[RES] = await asyncio.gather(*tasks)
    for task in tasks:
        res = await task
        print(f"time: {time.time() - start}")
        print('-'*20)
        print(res.code)
        if res.code != 0:
            print(res.msg)
        print(res.msg.split(r'installed corrected\n')[-1].split(r'\nResult')[0].strip())
        print(len(res.data))
        print(res.data[0].smiles)

if __name__ == "__main__":
    asyncio.run(test())

