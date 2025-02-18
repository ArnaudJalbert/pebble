from pebble.domain.entities import *


def test_import_entities() -> None:
    """
    Test that all entities can be imported.
    """
    assert Habit
    assert Recurrence
    assert Daily
    assert Weekly
    assert BiWeekly
    assert Monthly
    assert BiMonthly
    assert Yearly
    assert Quarterly
    assert WeekDays
