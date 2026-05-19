"""FastAPI 碳足迹计算 API."""

from fastapi import FastAPI, HTTPException
from .carbon_calculator import CarbonCalculator, IPCCModel, SheepParams
from .models import CalculateRequest, BatchRequest, CarbonReportResponse

app = FastAPI(title="CarbonFootprint API", version="2.0.0")


def _get_model(name: str) -> IPCCModel:
    try:
        return IPCCModel(name)
    except ValueError:
        raise HTTPException(400, f"Unknown model: {name}. Use 'tier1' or 'tier2'")


def _get_defaults(model: IPCCModel) -> dict:
    return CarbonCalculator.defaults(model)


@app.post("/calculate", response_model=CarbonReportResponse)
def calculate(req: CalculateRequest):
    model = _get_model(req.model)
    d = _get_defaults(model)
    params = SheepParams(
        area_km2=req.area_km2,
        grassland_factor=req.grassland_factor or d["grassland_factor"],
        manure_mass_t=req.manure_mass_t,
        manure_factor=req.manure_factor or d["manure_factor"],
        feed_emission_t=req.feed_emission_t or d["feed_emission"],
        enteric_emission_t=req.enteric_emission_t or d["enteric_emission"],
        energy_emission_t=req.energy_emission_t or d["energy_emission"],
        user_share=req.user_share,
        hold_years=req.hold_years,
    )
    report = CarbonCalculator.calculate(params, model)
    report.sheep_id = req.sheep_id
    return CarbonReportResponse(
        sheep_id=report.sheep_id,
        model=report.model.value,
        carbon_sink_tco2=report.carbon_sink,
        carbon_emission_tco2e=report.carbon_emission,
        net_credit_tco2e=report.net_credit,
        user_credit_tco2e=report.user_credit,
        detail=report.detail,
    )


@app.post("/batch")
def batch_calculate(req: BatchRequest):
    model = _get_model(req.model)
    results = []
    for sid in req.sheep_ids:
        report = CarbonCalculator.from_per_sheep(sheep_count=1, model=model)
        report.sheep_id = sid
        results.append({
            "sheep_id": sid,
            "net_credit_tco2e": report.net_credit,
            "user_credit_tco2e": report.user_credit,
        })
    return {"model": model.value, "count": len(results), "results": results}


@app.get("/report/{sheep_id}")
def get_report(sheep_id: str, model: str = "tier2"):
    m = _get_model(model)
    report = CarbonCalculator.from_per_sheep(sheep_count=1, model=m)
    report.sheep_id = sheep_id
    return CarbonReportResponse(
        sheep_id=report.sheep_id,
        model=report.model.value,
        carbon_sink_tco2=report.carbon_sink,
        carbon_emission_tco2e=report.carbon_emission,
        net_credit_tco2e=report.net_credit,
        user_credit_tco2e=report.user_credit,
        detail=report.detail,
    )


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}
