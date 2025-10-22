from fastmcp import FastMCP
from tools.base import (
    ADMET_predict,
    Pharmacokinetics_predict,
    ToxScan_predict,
    InputData,
    RES,
    AdmetInnerData,
    InputPK,
    PKResult,
    ToxResult
)
from tools.nmr import (
    NMR_search,
    NMR_predict,
    NMR_reverse_predict,
    SearchParam,
    PredictParam,
    ReversePredictParam,
    InputNMR,
    Result,
)
from structs.admet import description as admet_description
from structs.pk import description as pk_description

mcp = FastMCP("Demo 🚀")

@mcp.resource("data://ADMET_reference", name="ADMET Reference Data")
async def admet_meta():
    return {
        "name": "ADMET",
        "description": "ADMET is a collection of 20 molecular descriptors that are commonly used to predict the pharmacokinetic and pharmacodynamic properties of drugs.",
        "properties": admet_description
    }


@mcp.resource("data://Pharmacokinetics_reference", name="Pharmacokinetics Reference Data")
async def pk_meta():
    return {
        "name": "Pharmacokinetics",
        "description": "Pharmacokinetics is a collection of 10 molecular descriptors that are commonly used to predict the pharmacokinetic and pharmacodynamic properties of drugs.",
        "properties": pk_description
    }


# @mcp.tool(
#     name="ADMET_Service", 
#     description="Predict the ADMET properties of a molecule. Absorption, Distribution, Metabolism, Excretion and Toxicity Prediction for Molecules"
# )
# async def ADMET_predict_tool(data: InputData) -> RES[AdmetInnerData]:
#     return await ADMET_predict(data)


# @mcp.tool(
#     name="Pharmacokinetics_Service",
#     description="Predict the Pharmacokinetics properties of a molecule. Pharmacokinetic Metabolism Curve Prediction, Prediction of Drug Concentration Changes over Time."
# )
# async def Pharmacokinetics_predict_tool(data: InputPK) -> RES[PKResult]:
#     return await Pharmacokinetics_predict(data)


# @mcp.tool(
#     name="ToxScan_predict",
#     description="Predict the ToxScan properties of a molecule. Safety Evaluation of Drugs, Chemicals or Environmental Pollutants.",
# )
# async def ToxScan_predict_tool(data: InputData) -> RES[ToxResult]:
#     return await ToxScan_predict(data)

@mcp.tool(
    name="NMR_search",
    description="""Database search for molecules based on NMR spectroscopic data. For more accurate but slower reverse prediction, use NMR_reverse_predict tool.
    
    This tool performs molecular structure database searching using Nuclear Magnetic Resonance (NMR) spectroscopic data.
    Input 1H/13C NMR chemical shifts to find matching molecular structures from database. Allows constraints on elemental composition.
    
    Input:
        SearchParam

    Returns: List of candidate molecules with SMILES, predicted NMR data, and spectral similarity scores
    """,)
async def NMR_search_tool(data: SearchParam) -> RES[list[Result]]:
    try:
        if data is None:
            return RES(code=-1, msg="Invalid input: data cannot be None")
        else:
            result = await NMR_search(data)
            return result
        
    except Exception as e:
        return RES(code=-1, msg=f"nmr search error: {e}")

@mcp.tool(
    name="NMR_predict",
    description="""Predict NMR spectroscopic properties for molecular structures.
    
    This tool calculates simulated 1H and 13C NMR chemical shifts for given molecular structures.
    Input SMILES strings to simulate NMR spectra and validate structural assignments. Allows comparison of reference NMR spectra with predicted spectra for similarity scoring.
    
    Input:
        PredictParam
    
    Returns: List of molecules with predicted NMR chemical shifts and spectral similarity scores
    """,
)
async def NMR_predict_tool(data: PredictParam) -> RES[list[Result]]:
    try:
        if data is None:
            return RES(code=-1, msg="Invalid input: data cannot be None")
        else:
            result = await NMR_predict(data)
            return result
    
    except Exception as e:
        return RES(code=-1, msg=f"nmr predict error: {e}")

@mcp.tool(
    name="NMR_reverse_predict",
    description="""Reverse NMR analysis to propose molecular structures using molecular optimization. For fast database searching, use NMR_search tool.

    This tool generates candidate molecular structures from Nuclear Magnetic Resonance (NMR) spectroscopic data.
    Input 1H/13C NMR chemical shifts to identify compounds and determine structures. Allows constraints on elemental composition and molecular formula.

    Input:
        ReversePredictParam
    
    Returns: List of candidate molecules with SMILES, predicted NMR data, and spectral similarity scores
    """,
)
async def NMR_reverse_predict_tool(data: ReversePredictParam) -> RES[list[Result]]:
    try:
        if data is None:
            return RES(code=-1, msg="Invalid input: data cannot be None")
        else:
            result = await NMR_reverse_predict(data)
            return result

    except Exception as e:
        return RES(code=-1, msg=f"nmr reverse predict error: {e}")


if __name__ == "__main__":
    mcp.run(transport='sse',host="0.0.0.0",port=50003)
