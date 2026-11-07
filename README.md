# TWIN — Farm Digital Twin Engine

The simulation-engine half of **DigitalTwin-Agri**, the research behind the
IEEE paper *"DigitalTwin-Agri: A Hybrid Digital Twin Framework for
Next-Generation Smart Agriculture"*.

TWIN simulates a small farm as a grid of individual plants, each with its
own digital twin. A soil-moisture sensor twin watches each row, the farm
infers water stress from the sensor readings, and plant growth (leaf area
and biomass) advances day by day, slowed by that stress. On top of the
simulation sits a decision-support layer that can replay *what-if*
scenarios — for example, "what happens to leaf area if we irrigate the dry
row tomorrow?" — before any action is taken on the real farm.

## Architecture

| Package | What it contains |
|---|---|
| `FarmTwin/` | `FarmTwin` (`farm.py`) — the orchestrator. Builds the plant grid from `FarmGeometry` (rows × columns with spacing), keeps `GlobalTime`, attaches one soil-moisture sensor per row, and on `advance_time()` runs the loop: read sensors → infer water stress → update growth. `snapshot()` captures the whole farm state. |
| `PlantTwin/` | `PlantTwin` (`plant.py`) — one plant's twin, composed of dataclass states: growth (days after sowing, LAI, biomass, phenology stage), stress (water / thermal / nutrient), health, yield, spatial position and identity, plus a snapshot history. |
| `SensorTwin/` | The abstract `SensorTwin` base and `SoilMoistureSensorTwin`, which returns a row's soil-moisture percentage with Gaussian noise around a base value. `soil_moisture/inference.py` maps moisture to water stress: 0 at ≥ 45 % moisture, 1 at ≤ 30 %, linear in between. |
| `Models/growth/` | The growth model parameters and rules: base rates (`BASE_LAI_GROWTH_RATE = 0.05` per day, `BASE_BIOMASS_GROWTH_RATE = 1.0` per day) and `growth_reduction_factor()`, which turns water stress in [0, 1] into a growth multiplier (1 − stress). |
| `DecisionSupport/` | `IrrigationAction` (adds moisture to chosen rows), `run_scenario()` (deep-copies the farm and replays scheduled actions over a horizon without touching the live farm), the `average_lai()` growth metric, and a scenario-comparison visualisation. |
| `encoding.py`, `plot2d.py` | Map a plant snapshot to visual properties (size from LAI, colour green → orange → red from stress) and scatter-plot the farm. |
| `ui/streamlit/` | A Streamlit app (`app.py`) for interactive farm viewing and what-if scenarios — see "Known issues" below; it is partial work in progress. |

## Running it

The core engine needs only the Python standard library; `matplotlib` is
used for plotting and `streamlit` only for the UI.

```bash
pip install -r requirements.txt
```

The runnable, self-contained demo is the decision-support script. It
builds a 2 × 5 farm, makes row 0 dry, advances 5 days, then compares a
10-day no-irrigation scenario with irrigating row 0, printing the average
LAI for each:

```bash
python test_decision_irrigation.py
```

Other script-style demos at the repo root:

- `run_loop_view.py` — replay the farm day-by-day (15 days).
- `run_compare_view.py` — plot Day 0 vs Day 12 side by side.
- `run_animation_view.py` — animate 12 days of growth.
- `test_decision_visual.py` — visual version of the irrigation comparison.
- `test/test_visual_stress_growth.py` — a single visual stress/growth check.

## Known issues (as committed)

The visualisation scripts are honest work in progress:

- `run_loop_view.py`, `run_compare_view.py`, `run_animation_view.py`,
  `test/test_visual_stress_growth.py`, `test_decision_visual.py` and the
  Streamlit app import a `Visualization` package
  (`Visualization.encoding`, `Visualization.time.*`) that is **not present
  in this repository** — it only exists in the copy of this tree inside the
  [smartfarming](https://github.com/PrabhashNandan78/smartfarming) repo —
  so those scripts currently stop with `ModuleNotFoundError`. The core
  simulation and `test_decision_irrigation.py` do not depend on it and run
  as described above. Identical helpers also exist at this repo's root as
  `encoding.py` / `plot2d.py`.
- `ui/streamlit/app.py` additionally imports `ui.streamlit.views.*`, which
  is not in this repo, and the three files in `ui/streamlit/components/`
  are empty placeholders.

## The DigitalTwin-Agri family

- **[TWIN](https://github.com/PrabhashNandan78/TWIN)** (this repo) — the
  farm simulation engine.
- **[DIGITALTWIN_ML](https://github.com/PrabhashNandan78/DIGITALTWIN_ML)**
  — the ML notebooks and datasets behind the paper: groundnut yield
  modelling, the synthetic dataset, and the hybrid physics + ML approach.
- **[DT_ENGINE_SKELETON](https://github.com/PrabhashNandan78/DT_ENGINE_SKELETON)**
  — the earlier engine prototype that TWIN superseded.
- **[smartfarming](https://github.com/PrabhashNandan78/smartfarming)** — the
  original combined upload of all of the above.

## License

MIT — see [LICENSE](LICENSE).
