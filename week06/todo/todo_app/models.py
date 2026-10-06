from dataclasses import dataclass
from datetime import datetime

@dataclass
class Todo:
    id: int = None
    title: str = ""
    is_completed: bool = False
    created_at: datetime = None
