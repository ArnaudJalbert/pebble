from dataclasses import dataclass, field
from typing import Optional

from ..value_objects.types import ID, Description, Name
from .habit import Habit
from .habit_instance import HabitInstance


@dataclass
class HabitCollection:
    """
    This entity represents a collection of habits.
    It contains a name, a description, and a set of habits
    that belong to the collection.

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
    habits_instance: set[HabitInstance] = field(default_factory=lambda: set())
    id: Optional[ID] = None

    def add_habit(self, habit: Habit) -> None:
        """
        Adds a habit to the collection.

        Args:
            habit: The habit to be added to the collection.
        """
        if habit in self.habits:
            raise ValueError(f"Habit {habit.name} already exists in the collection")

        self.habits.add(habit)
