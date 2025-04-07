from datetime import date

import pytest
from mock_repository import MockRepository

from pebble.application.use_cases import CreateHabitInstance, CreateHabitInstanceDTO
from pebble.application.use_cases.create_habit_instance import (
    HabitInstanceCreationError,
)
from pebble.domain.entities import Daily, Habit, HabitCollection


@pytest.fixture
def test_habit_1() -> Habit:
    return Habit(
        id=1,
        name="Test Habit 1",
        recurrence=Daily(),
    )


@pytest.fixture
def test_habit_collection_1(test_habit_1: Habit) -> HabitCollection:
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
    test_habit_1: Habit,
    test_habit_collection_1: HabitCollection,
    mock_repository: MockRepository,
) -> None:
    """
    Test the creation of a habit instance.
    """
    habit_instance_dto = CreateHabitInstanceDTO(
        habit_id=test_habit_1.id,
        habit_collection_id=test_habit_collection_1.id,
        date=date.today(),
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


def test_create_habit_collection_habit_not_exist(
    mock_repository: MockRepository,
) -> None:
    """
    Test the creation of a habit instance with a non-existing habit.
    """
    habit_instance_dto = CreateHabitInstanceDTO(
        habit_id=999,  # Non-existing habit ID
        habit_collection_id=1,
        date=date.today(),
        completed=True,
        note="Test note",
    )

    with pytest.raises(HabitInstanceCreationError) as error_info:
        CreateHabitInstance(mock_repository).execute(habit_instance_dto)

    assert (
        str(error_info.value) == "Habit with ID 999 not found. "
        "The habit instance cannot be created without a Habit."
    )


def test_create_habit_collection_habit_collection_not_exist(
    mock_repository: MockRepository,
) -> None:
    """
    Test the creation of a habit instance with a non-existing habit collection.
    """
    habit_instance_dto = CreateHabitInstanceDTO(
        habit_id=1,
        habit_collection_id=999,  # Non-existing habit collection ID
        date=date.today(),
        completed=True,
        note="Test note",
    )

    with pytest.raises(HabitInstanceCreationError) as error_info:
        CreateHabitInstance(mock_repository).execute(habit_instance_dto)

    assert (
        str(error_info.value) == "Habit collection with ID 999 not found. "
        "The habit instance cannot be created without a Habit Collection."
    )


def test_create_habit_instance_future_date(
    test_habit_1: Habit,
    test_habit_collection_1: HabitCollection,
    mock_repository: MockRepository,
) -> None:
    """
    Test the creation of a habit instance with a future date.
    """
    habit_instance_dto = CreateHabitInstanceDTO(
        habit_id=test_habit_1.id,
        habit_collection_id=test_habit_collection_1.id,
        date=date.today().replace(year=2100),  # Future date
        completed=True,
        note="Test note",
    )

    with pytest.raises(HabitInstanceCreationError) as error_info:
        CreateHabitInstance(mock_repository).execute(habit_instance_dto)

    assert (
        str(error_info.value)
        == "Cannot create a habit instance for a future date: "
        + str(habit_instance_dto.date)
        + "."
    )
