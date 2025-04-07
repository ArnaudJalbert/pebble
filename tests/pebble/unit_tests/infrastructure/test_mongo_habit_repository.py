import mongomock
import pytest

from pebble.infrastructure.repositories import MongoHabitRepository


@pytest.fixture
def mock_mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()
    yield client


def test_mongo_habit_repository_instance(
    mock_mongo_client: mongomock.MongoClient,
) -> None:
    mongo_habit_repository = MongoHabitRepository(mock_mongo_client)

    # make sure they are defined, remove once they are implemented and tests
    mongo_habit_repository.save_habit(None)
    mongo_habit_repository.get_habit_by_id(None)
    mongo_habit_repository.get_habits_by_ids(None)
    mongo_habit_repository.save_habit_category(None)
    mongo_habit_repository.get_habit_category_by_name(None)
    mongo_habit_repository.save_habit_collection(None)
    mongo_habit_repository.update_habit_collection(None)
    mongo_habit_repository.get_habit_collection_by_id(None)
    mongo_habit_repository.save_habit_instance(None)
