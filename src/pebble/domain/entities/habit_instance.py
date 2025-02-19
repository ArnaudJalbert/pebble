from dataclasses import dataclass
from datetime import datetime

from pebble.domain.entities import Habit


@dataclass
class HabitInstance:
    habit: Habit
    date: datetime
    completed: bool
    notes: str
    id: int = None
