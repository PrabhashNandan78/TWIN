from PlantTwin.plant import PlantTwin
from FarmTwin.geometry.state import FarmGeometry
from FarmTwin.global_time.state import GlobalTime
from SensorTwin.soil_moisture.sensor import SoilMoistureSensorTwin
from SensorTwin.soil_moisture.inference import moisture_to_water_stress
from Models.growth.stress_response import growth_reduction_factor
from Models.growth.base_rates import (
    BASE_LAI_GROWTH_RATE,
    BASE_BIOMASS_GROWTH_RATE,
)


class FarmTwin:
    def __init__(
        self,
        farm_id: str,
        geometry: FarmGeometry
    ):
        self.farm_id = farm_id
        self.geometry = geometry
        self.global_time = GlobalTime()
        self.plants = []
        self.sensors = []
        self._initialize_soil_sensors()


        self._initialize_plants()

    def _initialize_plants(self):
        for r in range(self.geometry.num_rows):
            for c in range(self.geometry.num_cols):
                plant_id = f"P_{r}_{c}"
                x = c * self.geometry.col_spacing
                y = r * self.geometry.row_spacing

                plant = PlantTwin(
                    plant_id=plant_id,
                    row_index=r,
                    col_index=c,
                    x_coord=x,
                    y_coord=y
                )
                self.plants.append(plant)

    def advance_time(self, days: int = 1):
        self.global_time.advance(days)

       
        # Infer stress from sensors
        self.infer_water_stress()

        # Apply stress-modulated growth
        self.update_growth(days)


    def snapshot(self):
        return {
            "farm_id": self.farm_id,
            "day": self.global_time.day,
            "plants": [plant.snapshot() for plant in self.plants]
        }
    def _initialize_soil_sensors(self):
        """
        One soil moisture sensor per row
        """
        for row in range(self.geometry.num_rows):
            sensor = SoilMoistureSensorTwin(
                sensor_id=f"SM_ROW_{row}",
                attached_row=row,
                sampling_interval=1
            )
            self.sensors.append(sensor)
    def read_sensors(self):
        """
        Collect readings from all sensors
        """
        snapshot = self.snapshot()
        readings = []

        for sensor in self.sensors:
            reading = sensor.read(snapshot)
            readings.append(reading)

        return readings
    def infer_water_stress(self):
        readings = self.read_sensors()

        row_moisture = {
            r["row"]: r["soil_moisture_percent"]
            for r in readings
        }

       

        for plant in self.plants:
            row = plant.spatial.row_index
            moisture = row_moisture.get(row, 40.0)

            stress = moisture_to_water_stress(moisture)

            

            plant.update_state(
                stress_state={"water_stress": stress}
            )

    def update_growth(self, days: int = 1):
        for plant in self.plants:
            stress = plant.stress_state.water_stress
            reduction = growth_reduction_factor(stress)

            lai_increment = BASE_LAI_GROWTH_RATE * reduction * days
            biomass_increment = BASE_BIOMASS_GROWTH_RATE * reduction * days

            plant.update_state(
                growth_state={
                    "days_after_sowing":
                        plant.growth_state.days_after_sowing + days,
                    "LAI":
                        plant.growth_state.LAI + lai_increment,
                    "biomass":
                        plant.growth_state.biomass + biomass_increment,
                }
            )

