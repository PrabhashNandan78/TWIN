from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from Visualization.encoding import encode_plant_visual
from Visualization.plot2d import plot_farm

# Farm setup
geometry = FarmGeometry(2, 5, 0.5, 0.5)
farm = FarmTwin("FARM_VIS", geometry)

# Force drought on row 0
for sensor in farm.sensors:
    if sensor.attached_row == 0:
        sensor.base_moisture = 28.0   # severe stress
    else:
        sensor.base_moisture = 45.0   # healthy

# Advance time
farm.advance_time(days=12)

snapshot = farm.snapshot()

encoded = [
    encode_plant_visual(p) for p in snapshot["plants"]
]

plot_farm(
    encoded,
    title=f"Stress & Growth at Day {snapshot['day']}"
)
