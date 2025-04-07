from abc import ABC, abstractmethod
from typing import Set, Union

from pebble.domain.entities import Habit, HabitCategory, HabitCollection, HabitInstance
from pebble.domain.value_objects import ID


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
    def get_habit_by_id(self, habit_id: ID) -> Habit:
        """
        Gets a habit by identifier from the repository.

        Args:
            habit_id: The identifier of the habit to get.

        Returns:
            The habit with the provided identifier.

        Raises:
            RepositoryError: If the habit could not be found.
        """

    @abstractmethod
    def get_habits_by_ids(self, habits_ids: Set[ID]) -> Set[Habit]:
        """
        Gets a set of habits by identifiers from the repository.

        Args:
            habits_ids: A set of identifiers of the habits to get.

        Returns:
            A set of habits with the provided identifiers.

        Raises:
            RepositoryError: If the habits could not be found.
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
    def get_habit_category_by_name(
        self, category_name: str
    ) -> Union[HabitCategory, None]:
        """
        Gets a category by name from the repository.

        Args:
            category_name: The name of the category to get.

        Returns:
            The category with the provided name.

        Raises:
            RepositoryError: If the category could not be found.
        """

    @abstractmethod
    def save_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        """
        Saves a new habit collection in the repository.
        Assigns a unique identifier to the habit collection.

        Args:
            habit_collection: The habit collection to be saved.

        Returns:
            The saved habit collection, with the identifier.

        Raises:
            HabitCreationError: If the habit collection could not be created.
        """

    @abstractmethod
    def update_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        """
        Updates an existing habit collection in the repository.

        Args:
            habit_collection: The habit collection to be updated.

        Returns:
            The updated habit collection.

        Raises:
            RepositoryError: If the habit collection could not be updated.
        """

    @abstractmethod
    def get_habit_collection_by_id(self, habit_collection_id: ID) -> HabitCollection:
        """
        Gets a habit collection by identifier from the repository.

        Args:
            habit_collection_id: The identifier of the habit collection to get.

        Returns:
            The habit collection with the provided identifier.

        Raises:
            RepositoryError: If the habit collection could not be found.
        """

    @abstractmethod
    def save_habit_instance(self, habit_instance: HabitInstance) -> HabitInstance:
        """
        Saves a new habit instance in the repository.
        Assigns a unique identifier to the habit instance.

        Args:
            habit_instance: The habit instance to be saved.

        Returns:
            The saved habit instance, with the identifier.

        Raises:
            HabitCreationError: If the habit instance could not be created.
        """
