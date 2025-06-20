import datetime

import mongomock
import pytest
from bson import ObjectId

from pebble.application.serializers import HabitKVSerializer
from pebble.domain.entities import (
    Daily,
    Habit,
    HabitCategory,
    HabitCollection,
    HabitInstance,
)
from pebble.domain.value_objects import Color
from pebble.interface_adapters.repositories import MongoHabitRepository
from pebble.interface_adapters.repositories.mongo import MongoHabitExistsError
from pebble.interface_adapters.repositories.mongo.mongo_exceptions import (
    MongoHabitCategoryExistsError,
    MongoHabitCollectionExistsError,
    MongoHabitCollectionNotFoundError,
    MongoHabitNotFoundError,
)


@pytest.fixture
def mock_mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()
    yield client


@pytest.fixture
def mock_mongo_habit_repository(
    mock_mongo_client: mongomock.MongoClient,
) -> MongoHabitRepository:
    return MongoHabitRepository(mock_mongo_client)


@pytest.fixture
def generic_habit() -> Habit:
    habit_category = HabitCategory(
        name="Test Category",
        description="This is a test category",
        color=Color(hex="#FF5733"),
    )

    return Habit(
        name="Test Habit",
        recurrence=Daily(),
        description="This is a test habit",
        category=habit_category,
        color=Color(hex="#FF5733"),
    )


@pytest.fixture
def generic_habit_category() -> HabitCategory:
    return HabitCategory(
        name="Test Category",
        description="This is a test category",
        color=Color(hex="#FF5733"),
    )


@pytest.fixture
def generic_habit_collection() -> HabitCategory:
    return HabitCollection(
        name="Test Collection",
        description="This is a test collection",
    )


def test_save_habit(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit using the repository
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)

    # Check if the saved habit has an ID
    assert saved_habit.id is not None

    # Get the saved habit from the database
    saved_habit_data = mock_mongo_habit_repository.habits_collection.find_one(
        {"_id": ObjectId(saved_habit.id)}
    )

    # Check the IDs match
    assert saved_habit_data["_id"] == ObjectId(saved_habit.id)

    # Check if the saved habit data matches the original habit data
    saved_habit_dict = HabitKVSerializer.to_dict(saved_habit)
    del saved_habit_data["_id"]
    del saved_habit_dict["_id"]
    assert saved_habit_data == saved_habit_dict


def test_save_habit_already_exists(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit using the repository
    mock_mongo_habit_repository.save_habit(generic_habit)

    # Attempt to save the same habit again
    with pytest.raises(MongoHabitExistsError):
        mock_mongo_habit_repository.save_habit(generic_habit)


def test_get_habit_by_id(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
    generic_habit_category: HabitCategory,
) -> None:
    habit_category = mock_mongo_habit_repository.save_habit_category(
        generic_habit_category
    )
    generic_habit.category = habit_category
    mock_mongo_habit_repository.save_habit(generic_habit)

    fetched_habit: Habit = mock_mongo_habit_repository.get_habit_by_id(generic_habit.id)

    assert fetched_habit is not None
    assert generic_habit.id == fetched_habit.id
    assert generic_habit.category == fetched_habit.category


def test_get_habit_by_id_data_not_found(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
    generic_habit_category: HabitCategory,
) -> None:
    mock_mongo_habit_repository.save_habit_category(generic_habit_category)
    fetched_habit: Habit = mock_mongo_habit_repository.get_habit_by_id(generic_habit.id)

    assert fetched_habit is None


def test_get_habits_by_ids(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
    generic_habit_category: HabitCategory,
) -> None:
    other_habit = Habit(
        name="Other Habit",
        recurrence=Daily(),
        description="This is another test habit",
        category=generic_habit_category,
        color=Color(hex="#FF5733"),
    )
    mock_mongo_habit_repository.save_habit(generic_habit)
    mock_mongo_habit_repository.save_habit(other_habit)
    mock_mongo_habit_repository.save_habit_category(generic_habit_category)

    habits = mock_mongo_habit_repository.get_habits_by_ids(
        {generic_habit.id, other_habit.id}
    )

    assert len(habits) == 2
    assert generic_habit in habits
    assert other_habit in habits


def test_save_habit_category(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_category: HabitCategory,
) -> None:
    # Save the habit category using the repository
    saved_habit_category = mock_mongo_habit_repository.save_habit_category(
        generic_habit_category
    )

    assert saved_habit_category is not None
    assert saved_habit_category.id is not None
    assert saved_habit_category.name == generic_habit_category.name
    assert saved_habit_category.description == generic_habit_category.description
    assert saved_habit_category.color == generic_habit_category.color


def test_save_habit_category_already_exists(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_category: HabitCategory,
) -> None:
    # Save the habit category using the repository
    mock_mongo_habit_repository.save_habit_category(generic_habit_category)

    # Attempt to save the same habit category again
    with pytest.raises(MongoHabitCategoryExistsError):
        mock_mongo_habit_repository.save_habit_category(generic_habit_category)


def test_get_habit_category_by_name(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_category: HabitCategory,
) -> None:
    # Save the habit category using the repository
    saved_habit_category = mock_mongo_habit_repository.save_habit_category(
        generic_habit_category
    )

    # Get the habit category by name
    fetched_habit_category = mock_mongo_habit_repository.get_habit_category_by_name(
        saved_habit_category.name
    )

    assert fetched_habit_category is not None
    assert fetched_habit_category.id == saved_habit_category.id
    assert fetched_habit_category.name == saved_habit_category.name
    assert fetched_habit_category.description == saved_habit_category.description
    assert fetched_habit_category.color == saved_habit_category.color


def test_save_habit_collection(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_collection: HabitCollection,
    generic_habit: Habit,
) -> None:
    # Save the habit before saving the collection
    mock_mongo_habit_repository.save_habit(generic_habit)
    generic_habit_collection.add_habit(generic_habit)
    # Save the habit collection using the repository
    saved_habit_collection = mock_mongo_habit_repository.save_habit_collection(
        generic_habit_collection
    )

    assert saved_habit_collection is not None
    assert saved_habit_collection.id is not None
    assert saved_habit_collection.name == generic_habit_collection.name
    assert saved_habit_collection.description == generic_habit_collection.description
    assert len(saved_habit_collection.habits) == 1


def test_save_habit_collection_already_exists(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_collection: HabitCollection,
    generic_habit: Habit,
) -> None:
    # Save the habit before saving the collection
    mock_mongo_habit_repository.save_habit(generic_habit)
    generic_habit_collection.add_habit(generic_habit)
    # Save the habit collection using the repository
    fetched_habit_collection = mock_mongo_habit_repository.save_habit_collection(
        generic_habit_collection
    )

    # Attempt to save the same habit collection again
    with pytest.raises(MongoHabitCollectionExistsError):
        mock_mongo_habit_repository.save_habit_collection(fetched_habit_collection)


def test_save_habit_instance(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit before saving the instance
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)

    # Create a habit instance
    habit_instance = HabitInstance(
        habit=saved_habit,
        date=datetime.date(2023, 10, 1),
        completed=True,
        note="Test note",
    )

    # Save the habit instance using the repository
    saved_habit_instance = mock_mongo_habit_repository.save_habit_instance(
        habit_instance
    )

    assert saved_habit_instance is not None

    assert saved_habit_instance.id is not None
    assert saved_habit_instance.habit.id == saved_habit.id
    assert saved_habit_instance.date == habit_instance.date
    assert saved_habit_instance.completed == habit_instance.completed
    assert saved_habit_instance.note == habit_instance.note


def test_get_habit_instance_by_id(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit before saving the instance
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)

    # Create a habit instance
    habit_instance = HabitInstance(
        habit=saved_habit,
        date=datetime.date(2023, 10, 1),
        completed=True,
        note="Test note",
    )

    # Save the habit instance using the repository
    saved_habit_instance = mock_mongo_habit_repository.save_habit_instance(
        habit_instance
    )

    # Get the habit instance by ID
    fetched_habit_instance = mock_mongo_habit_repository.get_habit_instance_by_id(
        saved_habit_instance.id
    )

    assert fetched_habit_instance is not None
    assert fetched_habit_instance.id == saved_habit_instance.id
    assert fetched_habit_instance.habit.id == saved_habit.id
    assert fetched_habit_instance.date == habit_instance.date
    assert fetched_habit_instance.completed == habit_instance.completed
    assert fetched_habit_instance.note == habit_instance.note


def test_get_habit_collection_by_id(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_collection: HabitCollection,
    generic_habit: Habit,
) -> None:
    # Save the habit before saving the collection
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)
    generic_habit_collection.add_habit(saved_habit)

    # Save habit instances for the collection
    habit_instance = HabitInstance(
        habit=saved_habit,
        date=datetime.date(2023, 10, 1),
        completed=True,
        note="Test note",
    )
    mock_mongo_habit_repository.save_habit_instance(habit_instance)
    generic_habit_collection.habits_instance.add(habit_instance)

    # Save the habit collection using the repository
    saved_habit_collection = mock_mongo_habit_repository.save_habit_collection(
        generic_habit_collection
    )

    # Fetch the habit collection by ID
    fetched_habit_collection = mock_mongo_habit_repository.get_habit_collection_by_id(
        saved_habit_collection.id
    )

    assert fetched_habit_collection is not None
    assert fetched_habit_collection.id == saved_habit_collection.id
    assert fetched_habit_collection.name == saved_habit_collection.name
    assert fetched_habit_collection.description == saved_habit_collection.description
    assert len(fetched_habit_collection.habits) == len(saved_habit_collection.habits)
    assert fetched_habit_collection.habits == saved_habit_collection.habits
    assert (
        fetched_habit_collection.habits_instance
        == saved_habit_collection.habits_instance
    )


def test_save_habit_with_existing_id_raises_error(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit using the repository
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)

    # Attempt to save another habit with the same ID
    generic_habit.id = saved_habit.id
    with pytest.raises(MongoHabitExistsError):
        mock_mongo_habit_repository.save_habit(generic_habit)


def test_save_habit_instance_with_existing_id_raises_error(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit using the repository
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)

    # Create a habit instance
    habit_instance = HabitInstance(
        habit=saved_habit,
        date=datetime.date(2023, 10, 1),
        completed=True,
        note="Test note",
    )

    # Save the habit instance using the repository
    saved_habit_instance = mock_mongo_habit_repository.save_habit_instance(
        habit_instance
    )

    # Attempt to save another habit instance with the same ID
    habit_instance.id = saved_habit_instance.id
    with pytest.raises(MongoHabitExistsError):
        mock_mongo_habit_repository.save_habit_instance(habit_instance)


def test_get_habit_instance_by_id_not_found(
    mock_mongo_habit_repository: MongoHabitRepository,
) -> None:
    # Attempt to fetch a habit instance with a non-existent ID
    non_existent_id = str(ObjectId())
    fetched_habit_instance = mock_mongo_habit_repository.get_habit_instance_by_id(
        non_existent_id
    )

    # Assert that the result is None
    assert fetched_habit_instance is None


def test_get_habit_instance_by_id_habit_not_found(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit and create a habit instance
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)
    habit_instance = HabitInstance(
        habit=saved_habit,
        date=datetime.date(2023, 10, 1),
        completed=True,
        note="Test note",
    )
    saved_habit_instance = mock_mongo_habit_repository.save_habit_instance(
        habit_instance
    )

    # Remove the habit from the database
    mock_mongo_habit_repository.habits_collection.delete_one(
        {"_id": ObjectId(saved_habit.id)}
    )

    # Attempt to fetch the habit instance by ID
    with pytest.raises(MongoHabitNotFoundError):
        mock_mongo_habit_repository.get_habit_instance_by_id(saved_habit_instance.id)


def test_update_habit_collection(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_collection: HabitCollection,
    generic_habit: Habit,
) -> None:
    # Save the habit before saving the collection
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)
    generic_habit_collection.add_habit(saved_habit)

    # Save the habit collection using the repository
    saved_habit_collection = mock_mongo_habit_repository.save_habit_collection(
        generic_habit_collection
    )

    # Update the habit collection
    saved_habit_collection.name = "Updated Collection"
    updated_collection = mock_mongo_habit_repository.update_habit_collection(
        saved_habit_collection
    )

    # Assert the collection was updated successfully
    assert updated_collection.name == "Updated Collection"
    assert updated_collection.id == saved_habit_collection.id


def test_update_habit_collection_raises_error_when_not_found(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_collection: HabitCollection,
) -> None:
    # Attempt to update a non-existent habit collection
    generic_habit_collection.id = str(ObjectId())
    with pytest.raises(MongoHabitCollectionNotFoundError):
        mock_mongo_habit_repository.update_habit_collection(generic_habit_collection)


def test_update_habit_collection_raises_value_error_when_no_id(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit_collection: HabitCollection,
) -> None:
    # Ensure the habit collection does not have an ID
    generic_habit_collection.id = None

    # Attempt to update the habit collection and assert a ValueError is raised
    with pytest.raises(
        ValueError, match="Habit collection must have an ID to be updated."
    ):
        mock_mongo_habit_repository.update_habit_collection(generic_habit_collection)
