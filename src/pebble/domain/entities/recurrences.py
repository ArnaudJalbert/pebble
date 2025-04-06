from __future__ import annotations

from abc import ABC
from typing import Optional, Union

from ..value_objects.weekdays import WeekDays


class Recurrence(ABC):
    """
    Recurrence entity that represents the recurrence of a habit.

    This is the base entity for the Recurrence entity,
    concrete recurrences should inherit this class.

    The weekly_recurrence, monthly_recurrence, or yearly_recurrence
    should be set to the number of times the habit should recur
    in a week, month, or year respectively.

    Only one of the weekly_recurrence, monthly_recurrence,
    or yearly_recurrence should be set.

    Attributes:
        name: The name of the recurrence.
        weekly_recurrence: The number of times the habit should recur in a week.
        monthly_recurrence: The number of times the habit should recur in a month.
        yearly_recurrence: The number of times the habit should recur in a year.
    """

    name: str
    weekly_recurrence: Optional[int] = None
    monthly_recurrence: Optional[int] = None
    yearly_recurrence: Optional[int] = None

    def __init__(self, days_of_week: Optional[set[WeekDays]] = None) -> None:
        """
        Initializes the recurrence entity with the days of
        the week the habit should recur.

        Attributes:
            days_of_week: The day(s) of the week the habit should recur.

        Args:
            days_of_week: The day(s) of the week the habit should recur.
        """
        self._days_of_week: Union[set[WeekDays], None] = days_of_week

    def __str__(self) -> str:
        return f"{self.name} Recurrence"

    def __repr__(self) -> str:
        return (
            f"Name: {self.name} Recurrence "
            f"\nDays of the week: {self.days_of_week}"
            f"\nWeekly Recurrence: {self.weekly_recurrence}"
            f"\nMonthly Recurrence: {self.monthly_recurrence}"
            f"\nYearly Recurrence: {self.yearly_recurrence}"
        )

    @property
    def days_of_week(self) -> Union[set[WeekDays], None]:
        """
        Returns the day(s) of the week the habit should recur.

        Returns:
            The day(s) of the week the habit should recur.
        """
        return self._days_of_week

    @days_of_week.setter
    def days_of_week(self, days_of_week: set[WeekDays]) -> None:
        """
        Sets the day(s) of the week the habit should recur.

        Args:
            days_of_week: The day(s) of the week the habit should recur.
        """
        # Ensure that the days_of_week is a subset of all the days of the week.
        assert days_of_week.issubset(WeekDays.get_all())
        self._days_of_week = days_of_week

    def __eq__(self, other: Recurrence) -> bool:
        """
        Checks if the current recurrence is equal to another recurrence.

        Equality is based on the name, the recurrence amount,
        and days of the week of the recurrence.

        Args:
            other: The other recurrence to compare with.

        Returns:
            True if the current recurrence is equal to the other recurrence,
            False otherwise.
        """

        return (
            isinstance(other, Recurrence)
            and self.name == other.name
            and self.weekly_recurrence == other.weekly_recurrence
            and self.monthly_recurrence == other.monthly_recurrence
            and self.yearly_recurrence == other.yearly_recurrence
            and self.days_of_week == other.days_of_week
        )


class Daily(Recurrence):
    """
    Daily recurrence entity that represents the daily recurrence of a habit.
    """

    name = "Daily"
    weekly_recurrence = 7

    def __init__(self) -> None:
        super().__init__(WeekDays.get_all())

    @property
    def days_of_week(self) -> None:
        """
        Calls parent class's days_of_week property, only set to define the setter.
        """
        return super().days_of_week

    @days_of_week.setter
    def days_of_week(self, days_of_week: set[WeekDays]) -> None:
        """
        Raises an AttributeError since daily recurrence's days of the week
        can't be changed, it is always all days.
        Args:
            days_of_week: The day(s) of the week the habit should recur.
        """
        raise AttributeError(
            "Daily recurrence does not have a days_of_week attribute, "
            "it is always all days."
        )


class Weekly(Recurrence):
    """
    Weekly recurrence entity that represents the weekly recurrence of a habit.
    """

    name = "Weekly"
    weekly_recurrence = 1

    def __init__(self, days_of_week: Optional[set[WeekDays]] = None) -> None:
        """
        Initializes the weekly recurrence entity with the day(s) of the week
        the habit should recur.
        Checks that the number of days of the week is equal to the weekly recurrence.

        Args:
            days_of_week: The day(s) of the week the habit should recur.
        """
        assert len(days_of_week) == self.weekly_recurrence if days_of_week else True
        assert self.monthly_recurrence is None
        assert self.yearly_recurrence is None
        super().__init__(days_of_week)

    @property
    def days_of_week(self) -> set[WeekDays]:
        """
        Calls parent class's days_of_week property, only set to define the setter.
        """
        return super().days_of_week

    @days_of_week.setter
    def days_of_week(self, days_of_week: set[WeekDays]) -> None:
        """
        Sets the day(s) of the week the habit should recur.
        Checks that the number of days of the week is equal to the weekly recurrence.

        Args:
            days_of_week: The day(s) of the week the habit should recur.
        """
        assert len(days_of_week) == self.weekly_recurrence
        self._days_of_week = days_of_week


class BiWeekly(Weekly):
    """
    Bi-weekly recurrence entity that represents the bi-weekly recurrence of a habit.
    """

    name = "Bi-Weekly"
    weekly_recurrence = 2

    def __init__(self, days_of_week: Optional[set[WeekDays]] = None) -> None:
        super().__init__(
            days_of_week if days_of_week else {WeekDays.TUESDAY, WeekDays.FRIDAY}
        )


class Monthly(Recurrence):
    """
    Monthly recurrence entity that represents the monthly recurrence of a habit.
    """

    name = "Monthly"
    monthly_recurrence = 1
    yearly_recurrence = 12

    def __init__(self, days_of_week: Optional[set[WeekDays]] = None) -> None:
        assert len(days_of_week) == self.monthly_recurrence if days_of_week else True
        super().__init__(days_of_week)


class BiMonthly(Monthly):
    """
    Bi-monthly recurrence entity that represents the by-monthly recurrence of a habit.
    """

    name = "Bi-Monthly"
    monthly_recurrence = 2
    yearly_recurrence = 24


class Yearly(Recurrence):
    """
    Yearly recurrence entity that represents the yearly recurrence of a habit.
    """

    name = "Yearly"
    yearly_recurrence = 1

    def __init__(self, days_of_week: Optional[set[WeekDays]] = None) -> None:
        assert len(days_of_week) == 1 if days_of_week else True
        super().__init__(days_of_week)


class Quarterly(Yearly):
    """
    Quarterly recurrence entity that represents the quarterly recurrence of a habit.
    """

    name = "Quarterly"
    yearly_recurrence = 4
