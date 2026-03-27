from abc import ABC, abstractmethod

class SensorTwin(ABC):
    def __init__(self, sensor_id, sampling_interval):
        self.sensor_id = sensor_id
        self.sampling_interval = sampling_interval

    @abstractmethod
    def read(self, farm_snapshot):
        pass
