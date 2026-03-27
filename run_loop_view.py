from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from Visualization.time.loop import replay_farm_over_time

# --- Farm setup ---
geometry = FarmGeometry(
    num_rows=2,
    num_cols=5,
    row_spacing=0.5,
    col_spacing=0.5
)

farm = FarmTwin("FARM_LOOP", geometry)

# --- Stress scenario ---
for sensor in farm.sensors:
    if sensor.attached_row == 0:
        sensor.base_moisture = 28.0  # drought
    else:
        sensor.base_moisture = 45.0  # healthy

# --- Replay ---
replay_farm_over_time(
    farm=farm,
    days=15,
    delay=0.7
)
