import pytest

from pebble.domain.entities import BiMonthly, BiWeekly, Daily, Monthly, Weekly, Yearly
from pebble.domain.value_objects import WeekDays


def test_try_to_set_daily_days_of_week():
    with pytest.raises(AttributeError):
        Daily().days_of_week = {WeekDays.THURSDAY}


def test_try_to_set_incorrect_amount_of_weekdays():
    with pytest.raises(AssertionError):
        Weekly().days_of_week = {WeekDays.THURSDAY, WeekDays.FRIDAY, WeekDays.SATURDAY}


def test_set_weekly_days_of_week():
    weekly = Weekly()
    weekly.days_of_week = {WeekDays.THURSDAY}
    assert weekly.days_of_week == {WeekDays.THURSDAY}


def test_recurrences_name():
    assert str(Daily()) == "Daily Recurrence"
    assert str(Weekly()) == "Weekly Recurrence"
    assert str(BiWeekly()) == "Bi-Weekly Recurrence"
    assert str(Monthly()) == "Monthly Recurrence"
    assert str(BiMonthly()) == "Bi-Monthly Recurrence"
    assert str(Yearly()) == "Yearly Recurrence"


def test_assert_repr():
    assert repr(Daily()) is not None
    assert repr(Weekly()) is not None
    assert repr(BiWeekly()) is not None
    assert repr(Monthly()) is not None
    assert repr(BiMonthly()) is not None
    assert repr(Yearly()) is not None


def test_set_days_of_week():
    weekly = Monthly(days_of_week={WeekDays.FRIDAY})
    weekly.days_of_week = {WeekDays.THURSDAY}
    assert weekly.days_of_week == {WeekDays.THURSDAY}
