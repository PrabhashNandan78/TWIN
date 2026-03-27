import copy

from .plant_id.state import PlantIDState
from .spatial.state import SpatialState
from .growth_state.state import GrowthState
from .stress_state.state import StressState
from .health_state.state import HealthState
from .yield_state.state import YieldState
from .history.state import HistoryState


class PlantTwin:
    def __init__(
        self,
        plant_id: str,
        row_index: int,
        col_index: int,
        x_coord: float,
        y_coord: float,
    ):
        # Identity
        self.plant_id = PlantIDState(plant_id)

        # Spatial identity
        self.spatial = SpatialState(
            row_index=row_index,
            col_index=col_index,
            x_coord=x_coord,
            y_coord=y_coord
        )

        # Biological states
        self.growth_state = GrowthState()
        self.stress_state = StressState()
        self.health_state = HealthState()
        self.yield_state = YieldState()

        # Temporal memory
        self.history = HistoryState()

    def update_state(self, **kwargs):
        """
        Generic state update hook.
        Accepts named updates and routes them safely.
        """
        for state_name, updates in kwargs.items():
            state_obj = getattr(self, state_name, None)
            if state_obj is None:
                raise ValueError(f"Invalid state: {state_name}")

            for key, value in updates.items():
                if not hasattr(state_obj, key):
                    raise ValueError(
                        f"{key} not valid for {state_name}"
                    )
                setattr(state_obj, key, value)

    def snapshot(self):
        """
        Capture an IMMUTABLE snapshot of plant state.
        """
        snap = {
            "plant_id": self.plant_id.plant_id,
            "spatial": copy.deepcopy(vars(self.spatial)),
            "growth_state": copy.deepcopy(vars(self.growth_state)),
            "stress_state": copy.deepcopy(vars(self.stress_state)),
            "health_state": copy.deepcopy(vars(self.health_state)),
            "yield_state": copy.deepcopy(vars(self.yield_state)),
        }
        self.history.time_series.append(snap)
        return snap
