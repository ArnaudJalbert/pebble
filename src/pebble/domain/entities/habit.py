from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pebble.domain.entities import HabitCategory, Recurrence
from pebble.domain.value_objects import Color
from pebble.domain.value_objects.types import ID, Description, Name


@dataclass
class Habit:
    """
    Represents a habit. A habit is a task that is repeated over time.
    It contains a name, description, recurrence, category, and color.
    It indicates the frequency of the habit, the category it belongs to, and the color associated with it.

    Attributes:
        name: The name of the habit.
        recurrence: The recurrence of the habit.
        description: The description of the habit.
        category: The category of the habit.
        color: The color associated with the habit.
        id: The unique identifier of the habit.
    """

    name: Name
    recurrence: Recurrence
    description: Optional[Description] = None
    category: Optional[HabitCategory] = None
    color: Optional[Color] = None
    id: Optional[ID] = None

    def __eq__(self, other: Habit):
        if other.id is not None and self.id is not None:
            return self.id == other.id
        return (
            self.name == other.name
            and self.description == other.description
            and self.recurrence == other.recurrence
            and self.category == other.category
            and self.color == other.color
            and self.id == other.id
        )
