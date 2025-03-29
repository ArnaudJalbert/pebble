import pytest

from pebble.domain.value_objects import WeekDays
from mock_repository import MockRepository


@pytest.fixture
def habit_repository():
    return MockRepository()


def test_create_new_daily_habit(habit_repository):
    from pebble.application.use_cases.create_new_habit import (
        CreateNewHabit,
        CreateNewHabitDTO,
    )

    use_case = CreateNewHabit(habit_repository)
    dto = CreateNewHabitDTO(name="Test Habit", recurrence="Daily")
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 0

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 0
    assert len(habit_repository.get_category_by_name_calls) == 0

    # check the habit object
    assert habit.name == "Test Habit"
    assert habit.recurrence.name == "Daily"
    assert habit.category is None
    assert habit.color is None
    assert habit.id is not None


def test_create_new_weekly_habit(habit_repository):

    from pebble.application.use_cases.create_new_habit import (
        CreateNewHabit,
        CreateNewHabitDTO,
    )

    use_case = CreateNewHabit(habit_repository)
    dto = CreateNewHabitDTO(name="Test Habit", recurrence="Weekly")
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 0

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 0
    assert len(habit_repository.get_category_by_name_calls) == 0

    assert habit.name == "Test Habit"
    assert habit.recurrence.name == "Weekly"
    assert habit.recurrence.days_of_week is None
    assert habit.category is None
    assert habit.color is None
    assert habit.id is not None


def test_create_new_weekly_habit_with_weekday(habit_repository):
    from pebble.application.use_cases.create_new_habit import (
        CreateNewHabit,
        CreateNewHabitDTO,
    )

    use_case = CreateNewHabit(habit_repository)
    dto = CreateNewHabitDTO(
        name="Test Habit", recurrence="Weekly", recurrence_days={"Wednesday"}
    )
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 0

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 0
    assert len(habit_repository.get_category_by_name_calls) == 0

    assert habit.name == "Test Habit"
    assert habit.recurrence.name == "Weekly"
    assert habit.recurrence.days_of_week == {WeekDays.WEDNESDAY}
    assert habit.category is None
    assert habit.color is None
    assert habit.id is not None
