class IrrigationAction:
    """
    Represents an irrigation event applied at a specific day.
    """

    def __init__(self, target_rows, added_moisture):
        """
        target_rows    : list of row indices
        added_moisture : percentage points (e.g., +15%)
        """
        self.target_rows = target_rows
        self.added_moisture = added_moisture

    def apply(self, farm):
        """
        Apply irrigation by modifying soil moisture sensors.
        """
        for sensor in farm.sensors:
            if sensor.attached_row in self.target_rows:
                sensor.base_moisture = min(
                    100.0,
                    sensor.base_moisture + self.added_moisture
                )
