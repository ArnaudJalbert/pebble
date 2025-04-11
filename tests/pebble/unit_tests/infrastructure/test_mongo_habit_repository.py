import mongomock
import pytest
from bson import ObjectId

from pebble.application.serializers import HabitSerializer
from pebble.domain.entities import Daily, Habit, HabitCategory
from pebble.domain.value_objects import Color
from pebble.infrastructure.repositories import MongoHabitRepository
from pebble.infrastructure.repositories.mongo import MongoHabitExistsError


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
        id="123456",
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


def test_mongo_habit_repository_instance(
    mock_mongo_client: mongomock.MongoClient,
) -> None:
    mongo_habit_repository = MongoHabitRepository(mock_mongo_client)

    # make sure they are defined, remove once they are implemented and tested
    mongo_habit_repository.save_habit_category(None)
    mongo_habit_repository.get_habit_category_by_name(None)
    mongo_habit_repository.save_habit_collection(None)
    mongo_habit_repository.update_habit_collection(None)
    mongo_habit_repository.get_habit_collection_by_id(None)
    mongo_habit_repository.save_habit_instance(None)


def test_save_habit(
    mock_mongo_habit_repository: MongoHabitRepository,
    generic_habit: Habit,
) -> None:
    # Save the habit using the repository
    saved_habit = mock_mongo_habit_repository.save_habit(generic_habit)

    # Check if the saved habit has an ID
    assert saved_habit.id is not None

    # Get the saved habit from the database
    saved_habit_data = mock_mongo_habit_repository.habit_collection.find_one(
        {"_id": ObjectId(saved_habit.id)}
    )

    # Check the IDs match
    assert saved_habit_data["_id"] == ObjectId(saved_habit.id)

    # Check if the saved habit data matches the original habit data
    saved_habit_dict = HabitSerializer.to_dict(saved_habit)
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
    mock_mongo_habit_repository.save_habit(generic_habit)
    mock_mongo_habit_repository.save_habit_category(generic_habit_category)

    fetched_habit: Habit = mock_mongo_habit_repository.get_habit_by_id(generic_habit.id)

    assert fetched_habit is not None


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
