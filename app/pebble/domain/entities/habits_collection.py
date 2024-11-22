from dataclasses import dataclass, field
from typing import List, Optional

from pydantic import BaseModel

from .habit import Habit


class HabitsCollection(BaseModel):
    """
    HabitsCollection Entity that represents a collection of habits that a user wants to track.

    Attributes:
        name: The name of the collection.
        description: The description of the collection.
        habits: The list of habits that are part of the collection.
    """

    name: str
    description: Optional[str] = None
    habits: Optional[List[Habit]] = field(default_factory=list)

    def __iter__(self):
        return iter(self.habits)
