from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class TaskItem:
    task: str
    bucket: str = "🌟 MIT"  # "🌟 MIT", "📋 Secondary", "⚡ Quick Win"
    energy: str = "🔅 Medium"  # "🔋 High", "🔅 Medium", "🪫 Low"
    mode: str = "⚙️ Process"  # "🧠 Immersive", "⚙️ Process"
    area: str = "🗂️ Admin"  # "🎸 Teaching", "☁️ AWS SAA", "🎬 Chunnylab Lecture", "🏠 Life", "🗂️ Admin"
    time_block: str = ""
    est_minutes: int = 30
    subtasks: List[str] = field(default_factory=list)
    status: str = "To Do"  # "To Do", "Doing", "Done", "Dropped"


@dataclass
class DailyPlan:
    plan_date: date
    goal: str = ""
    cutoff_rule: str = ""
    tasks: List[TaskItem] = field(default_factory=list)
    notes: str = ""
    energy: str = "🔅 Medium"
    focus_hours: float = 0.0
    day_title: Optional[str] = None

    @property
    def title(self) -> str:
        if self.day_title:
            return self.day_title
        weekday_th = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][self.plan_date.weekday()]
        thai_year = self.plan_date.year + 543 if self.plan_date.year < 2500 else self.plan_date.year
        return f"{weekday_th} {self.plan_date.day} {self.plan_date.strftime('%b')} {thai_year}"

    @property
    def mit_tasks(self) -> List[TaskItem]:
        return [t for t in self.tasks if "MIT" in t.bucket]

    @property
    def secondary_tasks(self) -> List[TaskItem]:
        return [t for t in self.tasks if "Secondary" in t.bucket]

    @property
    def quick_wins(self) -> List[TaskItem]:
        return [t for t in self.tasks if "Quick" in t.bucket]
