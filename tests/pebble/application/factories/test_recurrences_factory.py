import pytest

from pebble.application.factories import (InvalidRecurrenceError,
                                          RecurrenceFactory)


def test_invalid_days_of_week():
    with pytest.raises(InvalidRecurrenceError):
        RecurrenceFactory.get_recurrence_from_strings(
            "Weekly", days_of_week={"invalid"}
        )
