from dataclasses import dataclass

@dataclass
class StressState:
    water_stress: float = 0.0
    thermal_stress: float = 0.0
    nutrient_stress: float = 0.0
