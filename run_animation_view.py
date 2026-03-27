from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from Visualization.time.animation import animate_farm

# --- Farm setup ---
geometry = FarmGeometry(
    num_rows=2,
    num_cols=5,
    row_spacing=0.5,
    col_spacing=0.5
)

farm = FarmTwin("FARM_ANIM", geometry)

# --- Stress scenario ---
for sensor in farm.sensors:
    if sensor.attached_row == 0:
        sensor.base_moisture = 28.0
    else:
        sensor.base_moisture = 45.0

# --- Simulate & collect history ---
history = []
history.append(farm.snapshot())

for _ in range(12):
    farm.advance_time(days=1)
    history.append(farm.snapshot())

# --- Animate ---
animate_farm(history, interval=700)
