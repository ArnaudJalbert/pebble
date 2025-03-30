from pebble.domain.entities import (BiMonthly, BiWeekly, Daily, Habit,
                                    HabitCategory, Monthly, Quarterly, Weekly,
                                    Yearly)
from pebble.domain.value_objects import Color, WeekDays


def test_create_daily_habit():
    habit = Habit(name="Test Habit", description="Test description", recurrence=Daily())
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Daily()
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_create_daily_habit_with_category():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=Daily(),
        category=HabitCategory(
            name="Test Category",
            description="Test description",
        ),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Daily()
    assert habit.category == HabitCategory(
        name="Test Category",
        description="Test description",
    )
    assert habit.color is None
    assert habit.id is None


def test_create_daily_habit_with_category_and_color():
    color = Color(hex="#FFFFFF")
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=Daily(),
        category=HabitCategory(
            name="Test Category",
            description="Test description",
            color=color,
        ),
        color=color,
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Daily()
    assert habit.category == HabitCategory(
        name="Test Category",
        description="Test description",
        color=color,
    )
    assert habit.color == color
    assert habit.id is None


def test_create_weekly_habit():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=Weekly(days_of_week={WeekDays.TUESDAY}),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Weekly(days_of_week={WeekDays.TUESDAY})
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_create_biweekly_habit():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=BiWeekly(days_of_week={WeekDays.TUESDAY, WeekDays.FRIDAY}),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == BiWeekly(
        days_of_week={WeekDays.TUESDAY, WeekDays.FRIDAY}
    )
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_create_monthly_habit():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=Monthly(days_of_week={WeekDays.TUESDAY}),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Monthly(days_of_week={WeekDays.TUESDAY})
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_create_bimonthly_habit():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=BiMonthly(days_of_week={WeekDays.TUESDAY, WeekDays.FRIDAY}),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == BiMonthly(
        days_of_week={WeekDays.TUESDAY, WeekDays.FRIDAY}
    )
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_create_yearly_habit():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=Yearly(days_of_week={WeekDays.TUESDAY}),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Yearly(days_of_week={WeekDays.TUESDAY})
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_create_quarterly_habit():
    habit = Habit(
        name="Test Habit",
        description="Test description",
        recurrence=Quarterly(days_of_week={WeekDays.TUESDAY}),
    )
    assert habit.name == "Test Habit"
    assert habit.description == "Test description"
    assert habit.recurrence == Quarterly(days_of_week={WeekDays.TUESDAY})
    assert habit.category is None
    assert habit.color is None
    assert habit.id is None


def test_habit_equality_without_id():
    habit1 = Habit(
        name="Test Habit", description="Test description", recurrence=Daily()
    )
    habit2 = Habit(
        name="Test Habit", description="Test description", recurrence=Daily()
    )
    assert habit1 == habit2


def test_habit_inequality_without_id():
    habit1 = Habit(
        name="Test Habit", description="Test description", recurrence=Daily()
    )
    habit2 = Habit(
        name="Another Habit", description="Another description", recurrence=Daily()
    )
    assert habit1 != habit2


def test_habit_equality_with_id():
    habit1 = Habit(
        name="Test Habit", description="Test description", recurrence=Daily(), id=1
    )
    habit2 = Habit(
        name="Another Habit",
        description="Another description",
        recurrence=Daily(),
        id=1,
    )
    assert habit1 == habit2


def test_habit_inequality_with_different_id():
    habit1 = Habit(
        name="Test Habit", description="Test description", recurrence=Daily(), id=1
    )
    habit2 = Habit(
        name="Test Habit", description="Test description", recurrence=Daily(), id=2
    )
    assert habit1 != habit2
