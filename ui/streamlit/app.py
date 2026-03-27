import streamlit as st
import time
import sys
import os

# Add parent directory to path so we can import twin(1) modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# =============================
# Core imports
# =============================
from FarmTwin.farm import FarmTwin
from FarmTwin.geometry.state import FarmGeometry
from Visualization.encoding import encode_plant_visual

from ui.streamlit.views.virtual_farm import render_virtual_farm
from ui.streamlit.views.virtual_farm_interactive import (
    render_virtual_farm_interactive
)

from DecisionSupport.actions.irrigation import IrrigationAction
from DecisionSupport.scenarios.runner import run_scenario
from DecisionSupport.metrics.growth_metrics import average_lai


# =============================
# Page config
# =============================
st.set_page_config(
    page_title="Smart Farming Digital Twin",
    layout="wide"
)

st.title("🌱 Smart Farming Digital Twin")
st.caption("Plant-level virtual replica of a real farm")


# =============================
# Initialize farm (ONCE)
# =============================
if "farm" not in st.session_state:
    geometry = FarmGeometry(
        num_rows=2,
        num_cols=5,
        row_spacing=0.5,
        col_spacing=0.5
    )

    farm = FarmTwin("FARM_UI", geometry)

    for sensor in farm.sensors:
        if sensor.attached_row == 0:
            sensor.base_moisture = 28.0
        else:
            sensor.base_moisture = 45.0

    st.session_state.farm = farm
    st.session_state.history = []


farm = st.session_state.farm


# =============================
# Sidebar — Time Control
# =============================
st.sidebar.header("⏱ Time Control")

days_to_advance = st.sidebar.slider(
    "Advance simulation by days",
    0, 30, 0, 1
)

if st.sidebar.button("Run Simulation"):
    for _ in range(days_to_advance):
        farm.advance_time(days=1)


# =============================
# Take snapshot & store history
# =============================
snapshot = farm.snapshot()

if (
    len(st.session_state.history) == 0
    or st.session_state.history[-1]["day"] != snapshot["day"]
):
    st.session_state.history.append(snapshot)

st.sidebar.divider()
st.sidebar.header("🧪 Replay Source")

replay_source = st.sidebar.radio(
    "Choose replay source",
    ["Live Farm", "Baseline Scenario", "Decision Scenario"]
)

# =============================
# Sidebar — Time Replay
# =============================
st.sidebar.divider()
st.sidebar.header("⏮️ Time Replay")

max_day = len(st.session_state.history) - 1

if max_day >= 1:
    replay_day = st.sidebar.slider(
        "Scrub Day",
        min_value=0,
        max_value=max_day,
        value=max_day,
        step=1
    )

    play = st.sidebar.button("▶ Play (auto)")
else:
    st.sidebar.info("Advance time to enable replay")
    replay_day = 0
    play = False
replay_speed = st.sidebar.slider(
    "Replay speed (seconds per day)",
    min_value=0.05,
    max_value=1.0,
    value=0.3,
    step=0.05
)


play = st.sidebar.button("▶ Play (auto)")
if play and max_day >= 1:
    for d in range(max_day + 1):
        st.session_state.replay_day = d
        time.sleep(replay_speed)




if replay_source == "Live Farm":
    history_source = st.session_state.history

elif replay_source == "Baseline Scenario" and "history_baseline" in st.session_state:
    history_source = st.session_state.history_baseline

elif replay_source == "Decision Scenario" and "history_decision" in st.session_state:
    history_source = st.session_state.history_decision

else:
    history_source = st.session_state.history  # fallback

max_day = len(history_source) - 1
replay_day = min(replay_day, max_day)

replay_snapshot = history_source[replay_day]


encoded_replay = [
    encode_plant_visual(p)
    for p in replay_snapshot["plants"]
]


# =============================
# View Mode
# =============================
st.subheader("🧭 Farm View")

view_mode = st.radio(
    "View Mode",
    ["Camera View", "Interactive View"],
    horizontal=True
)

# SIDEBAR - Camera Controls

st.sidebar.divider()
st.sidebar.header("🎥 Camera Control")

zoom = st.sidebar.slider(
    "Zoom",
    min_value=0.5,
    max_value=3.0,
    value=1.0,
    step=0.1
)

pan_x = st.sidebar.slider(
    "Pan X",
    min_value=-2.0,
    max_value=2.0,
    value=0.0,
    step=0.1
)

pan_y = st.sidebar.slider(
    "Pan Y",
    min_value=-2.0,
    max_value=2.0,
    value=0.0,
    step=0.1
)

# =============================
# Render Virtual Farm
# =============================
st.subheader(f"Farm — Day {replay_snapshot['day']}")

if view_mode == "Camera View":
    render_virtual_farm(
        encoded_replay,
        title=f"Farm — Day {replay_snapshot['day']}",
        zoom=zoom,
        pan_x=pan_x,
        pan_y=pan_y
    )

else:
    render_virtual_farm_interactive(replay_snapshot)


# =============================
# Sidebar — Decision Support
# =============================
st.sidebar.divider()
st.sidebar.header("💧 Decision Support")

target_rows = st.sidebar.multiselect(
    "Rows to irrigate",
    [0, 1],
    default=[0]
)

added_moisture = st.sidebar.slider(
    "Added soil moisture (%)",
    5, 40, 20, 5
)

decision_horizon = st.sidebar.slider(
    "Simulation horizon (days)",
    5, 30, 10, 1
)

run_decision = st.sidebar.button("Run What-If Scenario")


# =============================
# Run Decision Scenario
# =============================
if run_decision:
    irrigation = IrrigationAction(
        target_rows=target_rows,
        added_moisture=added_moisture
    )

    history_baseline = run_scenario(
        farm,
        {},
        farm.global_time.day,
        decision_horizon
    )

    history_decision = run_scenario(
        farm,
        {farm.global_time.day + 1: [irrigation]},
        farm.global_time.day,
        decision_horizon
    )

    st.session_state.history_baseline = history_baseline
    st.session_state.history_decision = history_decision

    st.success("Scenario simulation completed")


# =============================
# Decision Metrics
# =============================
if "history_decision" in st.session_state:
    st.subheader("📊 Decision Outcome")

    baseline_lai = average_lai(
        st.session_state.history_baseline, 0
    )

    decision_lai = average_lai(
        st.session_state.history_decision, 0
    )

    c1, c2 = st.columns(2)
    c1.metric("Baseline Avg LAI", f"{baseline_lai:.3f}")
    c2.metric("With Irrigation Avg LAI", f"{decision_lai:.3f}")


# =============================
# Plant Inspector (Phase 3A)
# =============================
st.sidebar.divider()
st.sidebar.header("🌱 Plant Inspector")

plant_ids = [
    p["plant_id"] for p in replay_snapshot["plants"]
]

selected_plant_id = st.sidebar.selectbox(
    "Select Plant",
    plant_ids
)

if selected_plant_id:
    plant = next(
        p for p in replay_snapshot["plants"]
        if p["plant_id"] == selected_plant_id
    )

    st.subheader(f"Plant Details — {selected_plant_id}")

    c1, c2, c3 = st.columns(3)

    c1.metric("LAI", round(plant["growth_state"]["LAI"], 3))
    c2.metric("Water Stress", round(plant["stress_state"]["water_stress"], 2))
    c3.metric("Health Score", round(plant["health_state"]["health_score"], 2))

    with st.expander("📍 Spatial & Growth Info"):
        st.json({
            "row": plant["spatial"]["row_index"],
            "col": plant["spatial"]["col_index"],
            "x": plant["spatial"]["x_coord"],
            "y": plant["spatial"]["y_coord"],
            "biomass": round(plant["growth_state"]["biomass"], 2),
            "phenology": plant["growth_state"]["phenology_stage"]
        })
