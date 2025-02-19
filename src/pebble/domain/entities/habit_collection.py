from dataclasses import dataclass, field

from pebble.domain.entities import Habit


@dataclass
class HabitCollection:

    name: str
    description: str
    habits: set[Habit] = field(default_factory=lambda: set())
    habits_instance: set[Habit] = field(default_factory=lambda: set())
    id: int = None
