import pytest
from setuptools.command.build_ext import use_stubs

from pebble.application.use_cases.create_habit_collection import (
    CreateHabitCollection,
    CreateHabitCollectionDTO,
)
from pebble.domain.entities import Habit, Daily
from mock_repository import MockRepository


@pytest.fixture
def habit_repository():
    return MockRepository()


def test_create_empty_habit_collection(habit_repository: MockRepository) -> None:
    use_case = CreateHabitCollection(habit_repository)

    dto = CreateHabitCollectionDTO(name="Test Habit Collection")

    habit_collection = use_case.execute(dto)

    assert len(habit_repository.get_habits_by_ids_calls) == 0
    assert len(habit_repository.save_habit_collection_calls) == 1
    assert habit_repository.save_habit_collection_calls[0].args[0] == habit_collection

    assert habit_collection.name == "Test Habit Collection"
    assert habit_collection.description is None
    assert habit_collection.habits == set()
    assert habit_collection.id is not None


def test_create_habit_collection_with_habits(habit_repository: MockRepository) -> None:

    habits = [
        Habit(
            name="Habit 1",
            recurrence=Daily(),
            category=None,
            color=None,
        ),
        Habit(
            name="Habit 2",
            recurrence=Daily(),
            category=None,
            color=None,
        ),
        Habit(
            name="Habit 3",
            recurrence=Daily(),
            category=None,
            color=None,
        ),
    ]

    for index, habit in enumerate(habits):
        habit_repository.save_habit(habit)
        habits[index] = habit

    use_case = CreateHabitCollection(habit_repository)

    dto = CreateHabitCollectionDTO(
        name="Test Habit Collection",
        description="A test habit collection",
        habits_ids={habit.id for habit in habit_repository.habits},
    )

    habit_collection = use_case.execute(dto)

    assert len(habit_repository.get_habits_by_ids_calls) == 1
    assert habit_repository.get_habits_by_ids_calls[0].args[0] == set(habits)
    assert len(habit_repository.save_habit_collection_calls) == 1
    assert habit_repository.save_habit_collection_calls[0].args[0] == habit_collection

    assert habit_collection.name == "Test Habit Collection"
    assert habit_collection.description == "A test habit collection"
    assert habit_collection.habits == set(habits)
    assert habit_collection.id is not None
