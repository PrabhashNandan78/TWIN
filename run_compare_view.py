from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from Visualization.time.compare import plot_side_by_side

geometry = FarmGeometry(
    num_rows=2,
    num_cols=5,
    row_spacing=0.5,
    col_spacing=0.5
)

farm = FarmTwin("FARM_COMPARE", geometry)

# Stress scenario
for sensor in farm.sensors:
    if sensor.attached_row == 0:
        sensor.base_moisture = 28.0
    else:
        sensor.base_moisture = 45.0

# --- Build history explicitly ---
history = []
history.append(farm.snapshot())  # TRUE Day 0

for day in range(12):
    farm.advance_time(days=1)
    history.append(farm.snapshot())
print(
    "Day", farm.global_time.day,
    "LAI row1:",
    [round(p.growth_state.LAI, 3)
     for p in farm.plants
     if p.spatial.row_index == 1]
)

# --- Compare TRUE states ---
snapshot_day_0 = history[0]
snapshot_day_12 = history[12]

plot_side_by_side(
    snapshot_day_0,
    snapshot_day_12,
    title_a="Day 0 (Initial State)",
    title_b="Day 12 (After Water Stress)"
)
