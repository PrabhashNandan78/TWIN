from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class HistoryState:
    time_series: List[Dict[str, Any]] = field(default_factory=list)
