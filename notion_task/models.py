from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class DailyPlan:
    plan_date: date
    priorities: List[str] = field(default_factory=list)
    secondary_tasks: List[str] = field(default_factory=list)
    quick_wins: List[str] = field(default_factory=list)
    notes: str = ""
    estimated_focus_hours: float = 0.0
