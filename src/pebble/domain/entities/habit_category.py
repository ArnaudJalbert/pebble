from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from pebble.domain.value_objects import Color
from pebble.domain.value_objects.types import Name, Description, ID


@dataclass
class HabitCategory:
    """
    This entity represents a category for a habit. It contains a name, a description, and an optional color.

    Attributes:
        name: The name of the category.
        description: The description of the category.
        color: The color of the category.
        id: The unique identifier of the category.
    """

    name: Name
    description: Optional[Description] = None
    color: Optional[Color] = None
    id: Optional[ID] = None

    def __eq__(self, other: HabitCategory) -> bool:
        if all(i is not None for i in (self.id, other.id)):
            return self.id == other.id
        return (
            self.name == other.name
            and self.description == other.description
            and self.color == other.color
            and self.id == other.id
        )
