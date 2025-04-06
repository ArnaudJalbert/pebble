from datetime import datetime

import pytest

from pebble.application.use_cases import CreateHabitInstance, CreateHabitInstanceDTO
from pebble.domain.entities import Habit, Daily, HabitCollection
from tests.pebble.unit_tests.application.use_cases.mock_repository import MockRepository


@pytest.fixture
def test_habit_1() -> Habit:
    return Habit(
        id=1,
        name="Test Habit 1",
        recurrence=Daily(),
    )


@pytest.fixture
def test_habit_collection_1(test_habit_1) -> HabitCollection:
    return HabitCollection(
        name="Test Habit Collection 1",
        habits={
            test_habit_1,
        },
        id=2,
    )


@pytest.fixture
def mock_repository(
    test_habit_1: Habit, test_habit_collection_1: HabitCollection
) -> MockRepository:
    mock_repository: MockRepository = MockRepository()
    mock_repository.save_habit(test_habit_1)
    mock_repository.save_habit_collection(test_habit_collection_1)

    return mock_repository


def test_create_habit_instance(
    test_habit_1, test_habit_collection_1, mock_repository
) -> None:
    """
    Test the creation of a habit instance.
    """
    habit_instance_dto = CreateHabitInstanceDTO(
        habit_id=test_habit_1.id,
        habit_collection_id=test_habit_collection_1.id,
        date=datetime.now(),
        completed=True,
        note="Test note",
    )
    habit_instance = CreateHabitInstance(mock_repository).execute(habit_instance_dto)

    # check repository calls

    # get habit by id call
    assert len(mock_repository.get_habit_by_id_calls) == 1
    assert mock_repository.get_habit_by_id_calls[0].args == [test_habit_1.id]
    assert mock_repository.get_habit_by_id_calls[0].return_value == test_habit_1

    # get habit collection by id call
    assert len(mock_repository.get_habit_collection_by_id_calls) == 1
    assert mock_repository.get_habit_collection_by_id_calls[0].args == [
        test_habit_collection_1.id
    ]
    assert (
        mock_repository.get_habit_collection_by_id_calls[0].return_value
        == test_habit_collection_1
    )

    # save habit instance call
    assert len(mock_repository.save_habit_instances_calls) == 1
    assert mock_repository.save_habit_instances_calls[0].args == [habit_instance]
    assert mock_repository.save_habit_instances_calls[0].return_value == habit_instance

    # check update of habit collection
    assert len(mock_repository.update_habit_collection_calls) == 1
    assert (
        mock_repository.update_habit_collection_calls[0].args[0]
        == test_habit_collection_1
    )
    assert (
        habit_instance
        in mock_repository.update_habit_collection_calls[0].args[0].habits_instance
    )

    assert habit_instance is not None
    assert habit_instance.habit == test_habit_1
    assert habit_instance.date == habit_instance_dto.date
    assert habit_instance.completed == habit_instance_dto.completed
    assert habit_instance.note == habit_instance_dto.note
    assert habit_instance.id is not None
    assert habit_instance in mock_repository.habit_instances
