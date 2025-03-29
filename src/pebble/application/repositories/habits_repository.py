from abc import ABC, abstractmethod
from typing import Union

from pebble.domain.entities import Habit, HabitCategory


class HabitCreationError(Exception):
    """Exception raised when a habit could not be created."""


class HabitRepository(ABC):

    @abstractmethod
    def save_habit(self, habit: Habit) -> Habit:
        """
        Saves a new habit in the repository.
        Assigns a unique identifier to the habit.

        Args:
            habit: The habit to be saved.

        Returns:
            The saved habit, with the identifier.

        Raises:
            HabitCreationError: If the habit could not be created.
        """

    @abstractmethod
    def save_habit_category(self, habit_category: HabitCategory) -> HabitCategory:
        """
        Creates a new habit category in the repository.
        Assigns a unique identifier to the category.

        Args:
            habit_category: The name of the category to be created.

        Returns:
            The created category, with the identifier.

        Raises:
            RepositoryError: If the category could not be created.
        """

    @abstractmethod
    def get_category_by_name(self, category_name: str) -> Union[HabitCategory, None]:
        """
        Gets a category by name from the repository.

        Args:
            category_name: The name of the category to get.

        Returns:
            The category with the provided name.

        Raises:
            RepositoryError: If the category could not be found.
        """
