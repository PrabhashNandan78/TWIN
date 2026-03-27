def average_lai(history, row_index):
    """
    Compute average LAI for a row over the scenario horizon.
    """
    total = 0.0
    count = 0

    for snap in history:
        for p in snap["plants"]:
            if p["spatial"]["row_index"] == row_index:
                total += p["growth_state"]["LAI"]
                count += 1

    return total / max(count, 1)
