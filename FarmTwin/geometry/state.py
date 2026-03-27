from dataclasses import dataclass

@dataclass
class FarmGeometry:
    num_rows: int
    num_cols: int
    row_spacing: float
    col_spacing: float
