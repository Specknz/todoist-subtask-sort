import datetime
from dataclasses import dataclass

@dataclass
class TaskOrder:
    id: str
    content: str
    due_date: datetime.date | None
    current_order: int
