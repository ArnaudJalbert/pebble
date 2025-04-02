from dataclasses import dataclass
from typing import Optional, Set

from pebble.application.repositories import HabitRepository
from pebble.domain.entities import HabitCollection
from pebble.domain.value_objects import ID


@dataclass
class CreateHabitCollectionDTO:
    """
    The DTO to create a habit collection.

    Attributes:
        name: The name of the habit collection.
        description: The description of the habit collection.
        habits_ids: The identifiers of the habits that the collection will have
    """

    name: str
    description: Optional[str] = None
    habits_ids: Set[ID] = None


class CreateHabitCollection:
    """
    Use case that creates a habit collection entity from a DTO.

    Creates the habit collection entity with the provided name, description, and habits.

    Links the habit collection with the habits provided in the DTO.

    Attributes:
        habit_repository: The repository that will be used to get the habits.
    """

    def __init__(self, habit_repository: HabitRepository) -> None:
        self.habit_repository: HabitRepository = habit_repository

    def execute(self, dto: CreateHabitCollectionDTO) -> HabitCollection:
        """
        Creates the habit collection entity with the
        provided name, description, and habits.

        Args:
            dto: The DTO with the data to create the habit collection.

        Returns:
            The habit collection entity created with a unique identifier.
        """
        habit_collection: HabitCollection = HabitCollection(
            name=dto.name,
            description=dto.description,
        )

        if dto.habits_ids:
            habits = self.habit_repository.get_habits_by_ids(dto.habits_ids)
            habit_collection.habits = habits

        self.habit_repository.save_habit_collection(habit_collection)

        return habit_collection
