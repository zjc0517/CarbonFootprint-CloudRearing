"""碳足迹计算引擎 — 支持 IPCC Tier1/Tier2 双模型，牧场级碳汇计算."""

from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class IPCCModel(Enum):
    TIER1 = "tier1"
    TIER2 = "tier2"


@dataclass
class SheepParams:
    area_km2: float
    grassland_factor: float
    manure_mass_t: float
    manure_factor: float
    feed_emission_t: float
    enteric_emission_t: float
    energy_emission_t: float
    user_share: float = 1.0
    hold_years: float = 1.0


@dataclass
class CarbonReport:
    sheep_id: str
    model: IPCCModel
    carbon_sink: float
    carbon_emission: float
    net_credit: float
    user_credit: float
    detail: dict


class CarbonCalculator:
    """碳足迹计算器，双IPCC模型.

    Tier1 — 全球默认排放因子，适合快速估算
    Tier2 — 中国北方温带草原区域因子，适合精确计算
    """

    TIER1 = {
        "grassland_factor": 120.0,   # tCO2/km²/yr (温带草原保守值)
        "manure_factor": 0.02,       # tCO2/t
        "feed_emission": 0.15,       # tCO2e/sheep/yr
        "enteric_emission": 0.25,    # tCO2e/sheep/yr
        "energy_emission": 0.05,     # tCO2e/sheep/yr
    }

    TIER2 = {
        "grassland_factor": 150.0,   # tCO2/km²/yr (内蒙古温带草原实测)
        "manure_factor": 0.028,      # tCO2/t
        "feed_emission": 0.08,       # tCO2e/sheep/yr (草原放牧为主)
        "enteric_emission": 0.25,    # tCO2e/sheep/yr
        "energy_emission": 0.03,     # tCO2e/sheep/yr
    }

    @classmethod
    def defaults(cls, model: IPCCModel) -> dict:
        return cls.TIER1 if model == IPCCModel.TIER1 else cls.TIER2

    @classmethod
    def calculate(cls, params: SheepParams, model: IPCCModel = IPCCModel.TIER2) -> CarbonReport:
        if not 0 <= params.user_share <= 1:
            raise ValueError("user_share must be in [0, 1]")
        if params.hold_years <= 0:
            raise ValueError("hold_years must be positive")

        sink = params.area_km2 * params.grassland_factor + params.manure_mass_t * params.manure_factor
        emission = params.feed_emission_t + params.enteric_emission_t + params.energy_emission_t
        net = sink - emission
        user_credit = round(net * params.user_share * params.hold_years, 4)

        return CarbonReport(
            sheep_id="",
            model=model,
            carbon_sink=round(sink, 4),
            carbon_emission=round(emission, 4),
            net_credit=round(net, 4),
            user_credit=user_credit,
            detail={
                "grassland_sink": round(params.area_km2 * params.grassland_factor, 4),
                "manure_sink": round(params.manure_mass_t * params.manure_factor, 4),
                "feed_emission": params.feed_emission_t,
                "enteric_emission": params.enteric_emission_t,
                "energy_emission": params.energy_emission_t,
            },
        )

    @classmethod
    def from_per_sheep(cls, sheep_count: int = 1, area_per_sheep: float = 0.006,
                       manure_per_sheep: float = 0.5, user_share: float = 1.0,
                       hold_years: float = 1.0, model: IPCCModel = IPCCModel.TIER2) -> CarbonReport:
        d = cls.defaults(model)
        params = SheepParams(
            area_km2=area_per_sheep * sheep_count,
            grassland_factor=d["grassland_factor"],
            manure_mass_t=manure_per_sheep * sheep_count,
            manure_factor=d["manure_factor"],
            feed_emission_t=d["feed_emission"] * sheep_count,
            enteric_emission_t=d["enteric_emission"] * sheep_count,
            energy_emission_t=d["energy_emission"] * sheep_count,
            user_share=user_share,
            hold_years=hold_years,
        )
        report = cls.calculate(params, model)
        report.sheep_id = f"batch-{sheep_count}"
        return report

    @classmethod
    def batch_calculate(cls, sheep_list: list[SheepParams],
                        model: IPCCModel = IPCCModel.TIER2) -> list[CarbonReport]:
        return [cls.calculate(p, model) for p in sheep_list]
