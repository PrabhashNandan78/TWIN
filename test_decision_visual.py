from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from DecisionSupport.actions.irrigation import IrrigationAction
from DecisionSupport.scenarios.runner import run_scenario
from DecisionSupport.visualization.compare_scenarios import plot_scenario_outcomes

geometry = FarmGeometry(2, 5, 0.5, 0.5)
farm = FarmTwin("FARM_DS_VIS", geometry)

# Initial drought
for sensor in farm.sensors:
    if sensor.attached_row == 0:
        sensor.base_moisture = 28.0
    else:
        sensor.base_moisture = 45.0

# Advance to Day 5
for _ in range(5):
    farm.advance_time(days=1)

# No irrigation
history_no = run_scenario(
    base_farm=farm,
    actions={},
    start_day=farm.global_time.day,
    horizon_days=10
)

# With irrigation
irrigation = IrrigationAction([0], 20.0)
history_yes = run_scenario(
    base_farm=farm,
    actions={farm.global_time.day + 1: [irrigation]},
    start_day=farm.global_time.day,
    horizon_days=10
)

plot_scenario_outcomes(
    history_no,
    history_yes,
    label_a="No Irrigation",
    label_b="Irrigation on Day 6"
)
