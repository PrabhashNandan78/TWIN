def encode_plant_visual(plant_snapshot):
    """
    Maps plant physiological state → visual properties
    """

    lai = plant_snapshot["growth_state"]["LAI"]
    stress = plant_snapshot["stress_state"]["water_stress"]

    # --- Size encoding (growth) ---
    # Ensure visibility even for small LAI
    
    MAX_EXPECTED_LAI = 1.0  # visual reference, not a claim

    normalized_lai = min(lai / MAX_EXPECTED_LAI, 1.0)

    # Strong perceptual amplification
    size = 0.2 + (normalized_lai * 2.5)


    # --- Color encoding (stress) ---
    # Green (no stress) → Red (max stress)
    if stress < 0.33:
        color = "green"
    elif stress < 0.66:
        color = "orange"
    else:
        color = "red"

    return {
        "x": plant_snapshot["spatial"]["x_coord"],
        "y": plant_snapshot["spatial"]["y_coord"],
        "size": size,
        "color": color,
        "stress": round(stress, 2),
        "LAI": round(lai, 2),
    }
