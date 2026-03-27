def moisture_to_water_stress(moisture_percent):
    """
    Maps soil moisture (%) to water stress [0–1]
    """
    if moisture_percent >= 45.0:
        return 0.0
    elif moisture_percent <= 30.0:
        return 1.0
    else:
        return (45.0 - moisture_percent) / 15.0
