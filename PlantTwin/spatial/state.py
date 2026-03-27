from dataclasses import dataclass

@dataclass
class SpatialState:
    row_index: int
    col_index: int
    x_coord: float
    y_coord: float
