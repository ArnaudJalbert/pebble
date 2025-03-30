import pytest

from pebble.application.factories import RecurrenceFactory
from pebble.application.factories.recurrence_factory import InvalidRecurrenceError


def test_invalid_days_of_week():
    with pytest.raises(InvalidRecurrenceError):
        RecurrenceFactory.get_recurrence_from_strings(
            "Weekly", days_of_week={"invalid"}
        )
