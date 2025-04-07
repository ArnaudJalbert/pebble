from dataclasses import dataclass
from datetime import date
from typing import Optional

from ..value_objects import ID, Note
from .habit import Habit


@dataclass
class HabitInstance:
    """
    This entity represents a habit instance, which is a habit
    that has been completed or not on a specific date.

    It tracks the habit, the date, whether it was completed, and an optional note.

    Attributes:
        habit: The habit that was completed or not.
        date: The date the habit was completed or not.
        completed: A boolean that indicates whether the habit was completed or not.
        note: An optional note about the habit.
        id: The unique identifier of the habit instance.
    """

    habit: Habit
    date: date
    completed: bool
    note: Optional[Note] = None
    id: Optional[ID] = None

    def __hash__(self) -> int:
        return hash(self.id)
