from dataclasses import dataclass

from pebble.domain.entities import Recurrence


@dataclass
class Habit:
    name: str
    description: str
    category: str
    recurrence: Recurrence
