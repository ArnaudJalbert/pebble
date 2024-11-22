import pytest
from typing import List

from pydantic import ValidationError

from pebble.domain.entities import HabitsCollection, Habit
from pebble.domain.entities.recurrence import *


TEST_NAME = "Test Habits Collection"
TEST_DESCRIPTION = "Test Description"


@pytest.fixture
def habits_list() -> List[Habit]:
    return [
        Habit(name="habit1", recurrence=Daily),
        Habit(name="habit2", recurrence=Weekly),
    ]


def test_create_habits_collection(habits_list: List[Habit]):
    empty_habits = HabitsCollection(
        name=TEST_NAME,
        description=TEST_DESCRIPTION,
    )
    assert empty_habits.habits == []
    assert empty_habits.name == TEST_NAME
    assert empty_habits.description == TEST_DESCRIPTION

    habits = HabitsCollection(name=TEST_NAME, habits=habits_list)
    assert habits.name == TEST_NAME
    assert habits.habits == habits_list

    # check that the habits are iterable
    for habit in habits:
        assert habit in habits_list


def test_create_habits_collection_wrong_arg():
    with pytest.raises(ValidationError):
        HabitsCollection(name=TEST_NAME, habits={"habit"})
