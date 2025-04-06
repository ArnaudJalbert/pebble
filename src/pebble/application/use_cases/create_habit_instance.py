from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pebble.application.repositories import HabitRepository
from pebble.domain.entities import Habit, HabitCollection, HabitInstance
from pebble.domain.value_objects import ID


@dataclass
class CreateHabitInstanceDTO:
    """
    This DTO is used to create a new habit instance.

    It contains the habit ID, the date, whether it was completed,
    and an optional note.

    Attributes:
        habit_id: The ID of the habit that was completed or not.
        date: The date the habit was completed or not.
        completed: A boolean that indicates whether the habit was completed or not.
        note: An optional note about the habit.
    """

    habit_id: ID
    habit_collection_id: ID
    date: datetime
    completed: bool
    note: Optional[str] = None


class HabitInstanceCreationError(Exception):
    """Exception raised when a habit instance could not be created."""


class CreateHabitInstance:
    """
    Use case for creating a new habit instance.

    This use case is responsible for creating a new habit instance and
    adding it to the corresponding habit collection.

    It checks if the habit exists, if the date is in the future,
    and if the habit collection exists before creating the habit instance.

    Attributes:
        habit_repository: The repository used to access and save habit instances.
    """

    def __init__(self, habit_repository: HabitRepository) -> None:
        self.habit_repository: HabitRepository = habit_repository

    def execute(self, dto: CreateHabitInstanceDTO) -> HabitInstance:
        """
        Creates a new habit instance.

        This method checks if the habit exists, if the date is in the future,
        and if the habit collection exists before creating the habit instance.

        Args:
            dto: The data transfer object containing the habit ID,
            date, completion status, and optional note.

        Returns:
            The created habit instance.

        Raises:
            HabitInstanceCreationError: If the habit instance could not be created.
        """
        # Check if the habit exists
        habit: Habit = self.habit_repository.get_habit_by_id(dto.habit_id)

        if habit is None:
            raise HabitInstanceCreationError(
                f"Habit with ID {dto.habit_id} not found."
                f"The habit instance cannot be created without a Habit."
            )

        # Check if the date is in the future, which is not allowed
        if dto.date > datetime.now():
            raise HabitInstanceCreationError(
                f"Cannot create a habit instance for a future date: {dto.date}."
            )

        # Create the habit instance
        habit_instance: HabitInstance = HabitInstance(
            habit=habit, date=dto.date, completed=dto.completed, note=dto.note
        )

        # Save the habit instance to the repository
        habit_instance = self.habit_repository.save_habit_instance(habit_instance)

        # Check if the habit collection exists
        habit_collection: HabitCollection = (
            self.habit_repository.get_habit_collection_by_id(dto.habit_collection_id)
        )

        if habit_collection is None:
            raise HabitInstanceCreationError(
                f"Habit collection with ID {dto.habit_collection_id} not found."
                f"The habit instance cannot be created without a Habit Collection."
            )

        # Add the habit instance to the habit collection
        habit_collection.habits_instance.add(habit_instance)

        # Update the habit collection in the repository with the new habit instance
        self.habit_repository.update_habit_collection(habit_collection)

        return habit_instance
