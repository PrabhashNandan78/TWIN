from dataclasses import dataclass

@dataclass
class HealthState:
    health_score: float = 1.0
    anomaly_flag: bool = False
