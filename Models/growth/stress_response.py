def growth_reduction_factor(water_stress: float) -> float:
    """
    Convert water stress [0–1] into growth reduction factor [0–1].

    0.0 stress → 1.0 (no reduction)
    1.0 stress → 0.0 (no growth)
    """
    water_stress = max(0.0, min(1.0, water_stress))
    return 1.0 - water_stress
