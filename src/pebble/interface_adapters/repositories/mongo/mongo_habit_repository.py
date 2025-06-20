from typing import Set, Union

from bson import ObjectId
from pymongo import MongoClient

from pebble.application.factories import RecurrenceFactory
from pebble.application.repositories import HabitRepository
from pebble.application.serializers import (
    HabitCategoryKVSerializer,
    HabitCollectionsKVSerializer,
    HabitInstanceKVSerializer,
    HabitKVSerializer,
)
from pebble.domain.entities import Habit, HabitCategory, HabitCollection, HabitInstance
from pebble.domain.value_objects import ID, Color

from .mongo_exceptions import (
    MongoHabitCategoryExistsError,
    MongoHabitCollectionExistsError,
    MongoHabitExistsError,
    MongoHabitNotFoundError,
)


class MongoHabitRepository(HabitRepository):
    DATABASE_NAME = "pebble"
    HABITS_COLLECTION_NAME = "habits"
    HABIT_CATEGORIES_COLLECTION_NAME = "habit_categories"
    HABIT_COLLECTIONS_COLLECTION_NAME = "habit_collections"
    HABIT_INSTANCE_COLLECTION_NAME = "habit_instances"

    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client
        self.db = mongo_client[self.DATABASE_NAME]
        self.habits_collection = self.db[self.HABITS_COLLECTION_NAME]
        self.habit_category_collection = self.db[self.HABIT_CATEGORIES_COLLECTION_NAME]
        self.habit_collections_collection = self.db[
            self.HABIT_COLLECTIONS_COLLECTION_NAME
        ]
        self.habit_instances_collection = self.db[self.HABIT_INSTANCE_COLLECTION_NAME]

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
        result = self.habits_collection.insert_one(habit_dict)
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
        habit_data = self.habits_collection.find_one({"_id": ObjectId(habit_id)})

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
        habits_data = self.habits_collection.find(
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
        """
        Saves a new habit collection in the repository.

        Saves a new habit collection in the MongoDB collection
        and assigns a unique identifier to the habit collection.

        Args:
            habit_collection: The habit collection to be saved.

        Returns:
            The saved habit collection, with the identifier.
        """
        # Check if the habit collection already exists in the database
        if self.get_habit_collection_by_id(habit_collection.id):
            raise MongoHabitCollectionExistsError(
                f"Habit collection with ID {habit_collection.id} already exists."
            )

        # Convert the habit collection to a dictionary and
        # insert it into the MongoDB collection.
        data = HabitCollectionsKVSerializer.to_dict(habit_collection)

        result = self.habit_collections_collection.insert_one(data)

        habit_collection.id = str(result.inserted_id)

        return habit_collection

    # Python
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
            ValueError: If the habit collection does not have an ID.
            MongoHabitCollectionExistsError: If the habit collection does not exist.
        """
        # Check if the habit collection has an ID
        if not habit_collection.id:
            raise ValueError("Habit collection must have an ID to be updated.")

        # Check if the habit collection exists in the database
        existing_collection = self.get_habit_collection_by_id(habit_collection.id)
        if not existing_collection:
            raise MongoHabitCollectionNotFoundError(
                f"Habit collection with ID {habit_collection.id} does not exist."
            )

        # Convert the habit collection to a dictionary
        habit_collection_dict = HabitCollectionsKVSerializer.to_dict(habit_collection)

        # Remove the `_id` field from the dictionary to avoid altering it
        habit_collection_dict.pop("_id", None)

        # Update the habit collection in the MongoDB collection
        self.habit_collections_collection.update_one(
            {"_id": ObjectId(habit_collection.id)},
            {"$set": habit_collection_dict},
        )

        return habit_collection

    def get_habit_collection_by_id(
        self, habit_collection_id: ID
    ) -> Union[HabitCollection, None]:
        """
        Gets a habit collection by identifier from the repository.

        Retrieves a habit collection from the MongoDB collection
        using the provided identifier.

        Args:
            habit_collection_id: The identifier of the habit collection to get.

        Returns:
            The habit collection with the provided identifier, if found, else None.
        """
        habit_collection_data = self.habit_collections_collection.find_one(
            {"_id": ObjectId(habit_collection_id)}
        )

        # If the habit collection is not found, return None
        if not habit_collection_data:
            return None

        # Recover the habits from the habit collection data
        habits_data = self.habits_collection.find(
            {
                "_id": {
                    "$in": [
                        ObjectId(habit_id)
                        for habit_id in habit_collection_data[
                            HabitCollectionsKVSerializer.DataKeys.HABITS
                        ]
                    ]
                }
            }
        )

        habits = set()

        for habit_data in habits_data:
            habits.add(self._habit_from_dict(habit_data))

        # Recover the habit instances from the habits data
        habit_instances_data = list(
            self.habit_instances_collection.find(
                {
                    HabitInstanceKVSerializer.DataKeys.HABIT_ID: {
                        "$in": [habit.id for habit in habits]
                    }
                }
            )
        )

        # Convert the habit instances data to HabitInstance objects
        habit_instances = set(
            (
                self.get_habit_instance_by_id(
                    habit_instance[HabitInstanceKVSerializer.DataKeys.ID]
                )
                for habit_instance in habit_instances_data
            )
        )

        return HabitCollectionsKVSerializer.from_dict(
            habit_collection_data, habits, habit_instances
        )

    def save_habit_instance(self, habit_instance: HabitInstance) -> HabitInstance:
        """
        Saves a new habit instance in the repository.

        Saves a new habit instance in the MongoDB collection
        and assigns a unique identifier to the habit instance.

        Args:
            habit_instance: The habit instance to be saved.

        Returns:
            The saved habit instance, with the identifier.
        """
        # Check if the habit instance already exists in the database
        if habit_instance.id and self.get_habit_instance_by_id(habit_instance.id):
            raise MongoHabitExistsError(
                f"Habit instance with ID {habit_instance.id} already exists."
            )

        # Convert the habit instance to a dictionary and
        # insert it into the MongoDB collection
        habit_instance_dict = HabitInstanceKVSerializer.to_dict(habit_instance)
        result = self.habit_instances_collection.insert_one(habit_instance_dict)
        habit_instance.id = str(result.inserted_id)

        return habit_instance

    def get_habit_instance_by_id(
        self, habit_instance_id: ID
    ) -> Union[HabitInstance, None]:
        """
        Gets a habit instance by identifier from the repository.

        Retrieves a habit instance from the MongoDB collection
        using the provided identifier.

        Args:
            habit_instance_id: The identifier of the habit instance to get.

        Returns:
            The habit instance with the provided identifier, if found, else None.
        """
        habit_instance_data = self.habit_instances_collection.find_one(
            {"_id": ObjectId(habit_instance_id)}
        )

        # If the habit instance is not found, return None
        if not habit_instance_data:
            return None

        habit = self.get_habit_by_id(
            habit_instance_data[HabitInstanceKVSerializer.DataKeys.HABIT_ID]
        )

        if not habit:
            raise MongoHabitNotFoundError(
                f"Error when trying to retrieve the habit instance "
                f"{habit_instance_data[HabitInstanceKVSerializer.DataKeys.ID]}. "
                f"Habit with ID "
                f"{habit_instance_data[HabitInstanceKVSerializer.DataKeys.HABIT_ID]} "
                f"does not exist."
            )

        return HabitInstanceKVSerializer.from_dict(habit_instance_data, habit)
