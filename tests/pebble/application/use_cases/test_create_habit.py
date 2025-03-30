import pytest
from mock_repository import MockRepository

from pebble.application.use_cases.create_habit import CreateHabit, CreateHabitDTO
from pebble.domain.entities import BiMonthly, HabitCategory
from pebble.domain.value_objects import Color, WeekDays


@pytest.fixture
def habit_repository():
    return MockRepository()


def test_create_new_daily_habit(habit_repository):
    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(name="Test Habit", recurrence="Daily")
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
    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(name="Test Habit", recurrence="Weekly")
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
    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(
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


def test_create_bi_weekly_habit_with_category(habit_repository):
    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(
        name="Test Habit",
        recurrence="Bi-Weekly",
        recurrence_days={"Wednesday", "Sunday"},
        category_name="Test Category",
    )
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 1

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 1
    assert len(habit_repository.get_category_by_name_calls) == 1

    assert habit.name == "Test Habit"
    assert habit.recurrence.name == "Bi-Weekly"
    assert habit.recurrence.days_of_week == {WeekDays.WEDNESDAY, WeekDays.SUNDAY}
    assert habit.category.name == "Test Category"
    assert habit.color is None
    assert habit.id is not None


def test_create_monthly_habit_with_category_and_color(habit_repository):
    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(
        name="Test Habit",
        recurrence="Monthly",
        recurrence_days={"Thursday"},
        category_name="Test Category",
        habit_color="#0e0e0e",
    )
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 1

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 1
    assert len(habit_repository.get_category_by_name_calls) == 1

    assert habit.name == "Test Habit"
    assert habit.recurrence.name == "Monthly"
    assert habit.recurrence.days_of_week == {WeekDays.THURSDAY}
    assert habit.category.name == "Test Category"
    assert habit.color == Color("#0e0e0e")
    assert habit.id is not None


def test_create_bi_monthly_habit_with_category_color(habit_repository):
    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(
        name="Test Habit",
        description="Habit Description",
        recurrence="Bi-Monthly",
        recurrence_days={"Tuesday", "Monday"},
        category_name="Test Category",
        habit_color="#0e0e0e",
        category_color="#33aa22",
        category_description="A Description",
    )
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 1

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 1
    assert len(habit_repository.get_category_by_name_calls) == 1

    assert habit.name == "Test Habit"
    assert isinstance(habit.recurrence, BiMonthly)
    assert habit.description == "Habit Description"
    assert habit.recurrence.days_of_week == {WeekDays.TUESDAY, WeekDays.MONDAY}
    assert habit.category.name == "Test Category"
    assert habit.color == Color("#0e0e0e")
    assert habit.category.color == Color("#33aa22")
    assert habit.category.description == "A Description"
    assert habit.id is not None


def test_create_habit_category_exists(habit_repository):
    habit_category = HabitCategory("Test Category", "A Description", Color("#33aa22"))
    habit_repository.categories.append(habit_category)

    use_case = CreateHabit(habit_repository)
    dto = CreateHabitDTO(
        name="Test Habit",
        recurrence="Bi-Monthly",
        description="Habit Description",
        category_name="Test Category",
        recurrence_days={"Tuesday", "Friday"},
    )
    habit = use_case.execute(dto)

    # check the data in repository
    assert len(habit_repository.habits) == 1
    assert len(habit_repository.categories) == 1

    # check the calls to the repository
    assert habit_repository.save_habit_calls[0].args[0] == habit
    assert habit_repository.save_habit_calls[0].return_value == habit
    assert len(habit_repository.save_habit_calls) == 1
    assert len(habit_repository.save_habit_category_calls) == 0
    assert len(habit_repository.get_category_by_name_calls) == 1

    assert habit.name == "Test Habit"
    assert isinstance(habit.recurrence, BiMonthly)
    assert habit.description == "Habit Description"
    assert habit.recurrence.days_of_week == {WeekDays.TUESDAY, WeekDays.FRIDAY}
    assert habit.category.name == "Test Category"
    assert habit.category.description == "A Description"
    assert habit.id is not None
