from dataclasses import dataclass, field
from typing import Optional

from pebble.domain.entities import Habit
from pebble.domain.value_objects.types import Name, Description, ID


@dataclass
class HabitCollection:
    """
    This entity represents a collection of habits. It contains a name, a description, and a set of habits that belong to
    the collection.

    Attributes:
        name: The name of the collection.
        description: The description of the collection.
        habits: A set of habits that belong to the collection.
        habits_instance: A set of habit instances that belong to the collection.
        id: The unique identifier of the collection
    """

    name: Name
    description: Optional[Description] = None
    habits: set[Habit] = field(default_factory=lambda: set())
    habits_instance: set[Habit] = field(default_factory=lambda: set())
    id: Optional[ID] = None
