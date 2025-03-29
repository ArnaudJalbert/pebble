from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pebble.domain.entities import Recurrence, HabitCategory
from pebble.domain.value_objects import Color
from pebble.domain.value_objects.types import Name, Description, ID




@dataclass
class Habit:
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
