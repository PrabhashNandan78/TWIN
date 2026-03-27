from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from DecisionSupport.actions.irrigation import IrrigationAction
from DecisionSupport.scenarios.runner import run_scenario
from DecisionSupport.metrics.growth_metrics import average_lai

# --- Base farm ---
geometry = FarmGeometry(2, 5, 0.5, 0.5)
farm = FarmTwin("FARM_DS", geometry)

# Initial drought
for sensor in farm.sensors:
    if sensor.attached_row == 0:
        sensor.base_moisture = 28.0
    else:
        sensor.base_moisture = 45.0

# Advance to Day 5 (current state)
for _ in range(5):
    farm.advance_time(days=1)

# --- Scenario A: no irrigation ---
history_no_irrig = run_scenario(
    base_farm=farm,
    actions={},
    start_day=farm.global_time.day,
    horizon_days=10
)

# --- Scenario B: irrigate row 0 on Day 6 ---
irrigation = IrrigationAction(
    target_rows=[0],
    added_moisture=20.0
)

history_irrig = run_scenario(
    base_farm=farm,
    actions={farm.global_time.day + 1: [irrigation]},
    start_day=farm.global_time.day,
    horizon_days=10
)

print(
    "Row 0 avg LAI (no irrigation):",
    round(average_lai(history_no_irrig, row_index=0), 3)
)
print(
    "Row 0 avg LAI (with irrigation):",
    round(average_lai(history_irrig, row_index=0), 3)
)
