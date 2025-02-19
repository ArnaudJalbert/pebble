from pebble.domain.value_objects import *


def test_import_value_objects() -> None:
    """
    Test that all value objects can be imported.
    """
    assert Color
    assert WeekDays
