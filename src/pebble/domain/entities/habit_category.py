from __future__ import annotations
from dataclasses import dataclass

from pebble.domain.value_objects import Color


@dataclass
class HabitCategory:
    name: str
    description: str
    color: Color = None
    id: int = None

    def __eq__(self, other: HabitCategory) -> bool:
        if all(i is not None for i in (self.id, other.id)):
            return self.id == other.id
        return (
            self.name == other.name
            and self.description == other.description
            and self.color == other.color
            and self.id == other.id
        )
