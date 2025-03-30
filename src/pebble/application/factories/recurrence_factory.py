from typing import Set

from pebble.domain.entities import (BiMonthly, BiWeekly, Daily, Monthly,
                                    Quarterly, Recurrence, Weekly, Yearly)
from pebble.domain.value_objects import WeekDays


class InvalidRecurrenceError(Exception):
    """
    Exception raised when an invalid recurrence is used.
    """


class RecurrenceFactory:
    ALL_RECURRENCES = {Daily, Weekly, BiWeekly, Monthly, BiMonthly, Yearly, Quarterly}
    ALL_RECURRENCES_BY_NAME = {
        recurrence.name: recurrence for recurrence in ALL_RECURRENCES
    }

    @classmethod
    def get_recurrence_from_strings(
        cls, recurrence_name: str, days_of_week: Set[str]
    ) -> Recurrence:

        # A daily recurrence is the default recurrence, no weekday is needed
        if recurrence_name.lower() == "daily":
            return Daily()

        # validate the days provided for recurrence
        if days_of_week and not all(
            WeekDays.valid_weekday(day) for day in days_of_week
        ):
            raise InvalidRecurrenceError("Invalid days provided for recurrence")

        # create a set of WeekDays objects from the days provided in the DTO
        recurrence_days: Set[WeekDays] = (
            {WeekDays(day) for day in days_of_week} if days_of_week else None
        )

        return cls.ALL_RECURRENCES_BY_NAME[recurrence_name](recurrence_days)
