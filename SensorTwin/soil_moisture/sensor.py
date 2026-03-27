import random
from SensorTwin.base.sensor import SensorTwin


class SoilMoistureSensorTwin(SensorTwin):
    def __init__(
        self,
        sensor_id,
        attached_row,
        sampling_interval=1,
        base_moisture=40.0,
        noise_std=2.0
    ):
        super().__init__(sensor_id, sampling_interval)
        self.attached_row = attached_row
        self.base_moisture = base_moisture
        self.noise_std = noise_std

    def read(self, farm_snapshot):
        """
        Returns soil moisture percentage for a row
        """
        noise = random.gauss(0, self.noise_std)
        moisture = max(
            0.0,
            min(100.0, self.base_moisture + noise)
        )

        return {
            "sensor_id": self.sensor_id,
            "row": self.attached_row,
            "soil_moisture_percent": moisture
        }
