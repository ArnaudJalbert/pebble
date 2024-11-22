import pytest
from datetime import datetime
from pydantic import ValidationError

from pebble.domain.entities import Habit
from pebble.domain.entities.recurrence import Weekly

TEST_NAME = "Test Habit"
TEST_DESCRIPTION = "Test Description"
TEST_RECURRENCE = Weekly
TEST_ID = 1
TEST_USER_ID = 2
TEST_CREATED_AT = datetime(2021, 1, 1)
TEST_UPDATED_AT = datetime(2021, 1, 5)


def test_habit():

    habit = Habit(
        name=TEST_NAME,
        description=TEST_DESCRIPTION,
        recurrence=TEST_RECURRENCE,
        id=TEST_ID,
        user_id=TEST_USER_ID,
        created_at=TEST_CREATED_AT,
        updated_at=TEST_UPDATED_AT,
    )

    assert habit.name == TEST_NAME
    assert isinstance(habit.name, str)
    assert habit.description == TEST_DESCRIPTION
    assert isinstance(habit.description, str)
    assert habit.recurrence == TEST_RECURRENCE
    assert isinstance(habit.recurrence, type)
    assert habit.id == TEST_ID
    assert isinstance(habit.id, int)
    assert habit.user_id == TEST_USER_ID
    assert isinstance(habit.user_id, int)
    assert habit.created_at == TEST_CREATED_AT
    assert isinstance(habit.created_at, datetime)
    assert habit.updated_at == TEST_UPDATED_AT
    assert isinstance(habit.updated_at, datetime)


def test_habit_wrong_type():

    with pytest.raises(ValidationError):
        Habit(
            name=TEST_NAME,
            description=TEST_DESCRIPTION,
            recurrence="Weekly",
            id=TEST_ID,
            user_id=TEST_USER_ID,
            created_at=TEST_CREATED_AT,
            updated_at=TEST_UPDATED_AT,
        )