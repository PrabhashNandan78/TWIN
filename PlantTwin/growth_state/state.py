from dataclasses import dataclass

@dataclass
class GrowthState:
    days_after_sowing: int = 0
    LAI: float = 0.0
    biomass: float = 0.0
    phenology_stage: str = "emergence"
