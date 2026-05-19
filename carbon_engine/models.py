"""数据模型."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SheepRecord(BaseModel):
    sheep_id: str = Field(..., description="羊只唯一标识 RG-SH-YYYYMMDD-XXXXXXXX")
    breed: str
    ranch_id: str
    birth_date: str
    weight_kg: float = 0.0
    area_km2: float = 0.001
    manure_mass_t: float = 0.5
    user_share: float = 1.0
    hold_years: float = 1.0


class CalculateRequest(BaseModel):
    sheep_id: str
    area_km2: float = 0.001
    grassland_factor: Optional[float] = None
    manure_mass_t: float = 0.5
    manure_factor: Optional[float] = None
    feed_emission_t: Optional[float] = None
    enteric_emission_t: Optional[float] = None
    energy_emission_t: Optional[float] = None
    user_share: float = 1.0
    hold_years: float = 1.0
    model: str = "tier2"


class BatchRequest(BaseModel):
    sheep_ids: list[str]
    model: str = "tier2"


class CarbonReportResponse(BaseModel):
    sheep_id: str
    model: str
    carbon_sink_tco2: float
    carbon_emission_tco2e: float
    net_credit_tco2e: float
    user_credit_tco2e: float
    detail: dict
    calculated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
