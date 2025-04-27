from typing import Set, Union

from bson import ObjectId
from pymongo import MongoClient

from pebble.application.factories import RecurrenceFactory
from pebble.application.repositories import HabitRepository
from pebble.application.serializers import HabitCategoryKVSerializer, HabitKVSerializer
from pebble.domain.entities import Habit, HabitCategory, HabitCollection, HabitInstance
from pebble.domain.value_objects import ID, Color

from .mongo_exceptions import MongoHabitCategoryExistsError, MongoHabitExistsError


class MongoHabitRepository(HabitRepository):
    DATABASE_NAME = "pebble"
    HABIT_COLLECTION_NAME = "habits"
    HABIT_CATEGORIES_COLLECTION_NAME = "habit_categories"

    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client[self.DATABASE_NAME]
        self.habit_collection = self.db[self.HABIT_COLLECTION_NAME]
        self.habit_category_collection = self.db[self.HABIT_CATEGORIES_COLLECTION_NAME]

    def _habit_from_dict(self, habit_data: dict) -> Habit:
        # recover the recurrence from the habit data with the factory
        recurrence = RecurrenceFactory.get_recurrence_from_strings(
            habit_data[HabitKVSerializer.DataKeys.RECURRENCE],
            habit_data[HabitKVSerializer.DataKeys.RECURRENCE_DAYS],
        )

        category_id: str = habit_data[HabitKVSerializer.DataKeys.CATEGORY_ID]
        habit_category: HabitCategory = None

        if category_id:
            # recover the habit category from the habit data
            habit_category_data = self.habit_category_collection.find_one(
                {"_id": ObjectId(habit_data[HabitKVSerializer.DataKeys.CATEGORY_ID])}
            )
            habit_category = HabitCategoryKVSerializer.from_dict(habit_category_data)

        return Habit(
            name=habit_data[HabitKVSerializer.DataKeys.NAME],
            recurrence=recurrence,
            description=habit_data[HabitKVSerializer.DataKeys.DESCRIPTION],
            category=habit_category,
            color=Color(habit_data[HabitKVSerializer.DataKeys.COLOR_HEX]),
            id=str(habit_data[HabitKVSerializer.DataKeys.ID]),
        )

    def save_habit(self, habit: Habit) -> Habit:
        """
        Saves a new habit in the repository.

        Saves a new habit in the MongoDB collection
        and assigns a unique identifier to the habit.

        Args:
            habit: The habit to be saved.

        Returns:
            The saved habit, with the identifier.

        Raises:

        """
        # Check if the habit already exists in the database
        if habit.id and self.get_habit_by_id(habit.id):
            raise MongoHabitExistsError(f"Habit with ID {habit.id} already exists.")

        # Convert the habit to a dictionary and insert it into the MongoDB collection
        habit_dict = HabitKVSerializer.to_dict(habit)
        result = self.habit_collection.insert_one(habit_dict)
        habit.id = str(result.inserted_id)

        return habit

    def get_habit_by_id(self, habit_id: str) -> Union[Habit, None]:
        """
        Gets a habit by identifier from the repository.

        Retrieves a habit from the MongoDB collection
        using the provided identifier.

        Args:
            habit_id: The identifier of the habit to get.

        Returns:
            The habit with the provided identifier, if found, else None.
        """
        habit_data = self.habit_collection.find_one({"_id": ObjectId(habit_id)})

        # If the habit is not found, return None
        if not habit_data:
            return None

        return self._habit_from_dict(habit_data)

    def get_habits_by_ids(self, habits_ids: Set[ID]) -> Set[Habit]:
        """
        Gets a set of habits by their identifiers from the repository.

        Retrieves a set of habits from the MongoDB collection
        using the provided identifiers.

        Args:
            habits_ids: The identifiers of the habits to get.

        Returns:
            The set of habits with the provided identifiers.
        """
        habits_data = self.habit_collection.find(
            {"_id": {"$in": [ObjectId(habit_id) for habit_id in habits_ids]}}
        )

        habits = set()

        for habit_data in habits_data:
            habits.add(self._habit_from_dict(habit_data))

        return habits

    def save_habit_category(self, habit_category: HabitCategory) -> HabitCategory:
        """
        Saves a new habit category in the repository.
        Args:
            habit_category: The habit category to be saved.

        Returns:
            The saved habit category, with the identifier.

        Raises:
            MongoHabitCategoryExistsError: If the habit category already exists.
        """
        # Check if the habit category already exists in the database
        if self.get_habit_category_by_name(habit_category.name):
            raise MongoHabitCategoryExistsError(
                f"Habit category with name {habit_category.name} already exists."
            )

        # Convert the habit category to a dictionary and
        # insert it into the MongoDB collection
        habit_category_dict = HabitCategoryKVSerializer.to_dict(habit_category)
        result = self.habit_category_collection.insert_one(habit_category_dict)
        habit_category.id = str(result.inserted_id)

        return habit_category

    def get_habit_category_by_name(
        self, category_name: str
    ) -> Union[HabitCategory, None]:
        """
        Gets a habit category by name from the repository.

        Retrieves a habit category from the MongoDB collection
        using the provided name.

        Args:
            category_name: The name of the habit category to get.

        Returns:
            The habit category with the provided name, if found, else None.
        """
        # Retrieve the habit category from the MongoDB collection
        data = self.habit_category_collection.find_one({"name": category_name})

        # If the habit category is not found, return None
        if not data:
            return None

        # Convert the habit category data to a HabitCategory object
        return HabitCategoryKVSerializer.from_dict(data)

    def save_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        pass

    def update_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        pass

    def get_habit_collection_by_id(self, habit_collection_id: ID) -> HabitCollection:
        pass

    def save_habit_instance(self, habit_instance: HabitInstance) -> HabitInstance:
        pass
