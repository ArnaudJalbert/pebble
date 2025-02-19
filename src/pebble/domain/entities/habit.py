from dataclasses import dataclass

from pebble.domain.entities import Recurrence, HabitCategory
from pebble.domain.value_objects import Color


@dataclass
class Habit:
    name: str
    description: str
    recurrence: Recurrence
    category: HabitCategory = None
    color: Color = None
    id: int = None

    def __eq__(self, other):
        if all(i is not None for i in (self.id, other.id)):
            return self.id == other.id
        return (
            self.name == other.name
            and self.description == other.description
            and self.recurrence == other.recurrence
            and self.category == other.category
            and self.color == other.color
            and self.id == other.id
        )
