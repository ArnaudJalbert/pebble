from __future__ import annotations

from enum import Enum


class WeekDays(Enum):
    MONDAY: str = "Monday"
    TUESDAY: str = "Tuesday"
    WEDNESDAY: str = "Wednesday"
    THURSDAY: str = "Thursday"
    FRIDAY: str = "Friday"
    SATURDAY: str = "Saturday"
    SUNDAY: str = "Sunday"

    @classmethod
    def get_all(cls) -> set[WeekDays]:
        return {day for day in cls}

    @classmethod
    def valid_weekday(cls, day: str) -> bool:
        return day in cls._value2member_map_
