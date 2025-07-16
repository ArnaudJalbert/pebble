import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Union

from pebble.application.repositories import HabitRepository


class RetrieveHabitsInTimeFrame:
    """
    Use case for retrieving habits within a specified time frame.
    """

    @dataclass(frozen=True, slots=True, kw_only=True)
    class InputData:
        start_date: datetime
        end_date: datetime

    @dataclass(frozen=True, slots=True, kw_only=True)
    class OutputData:
        habits: Dict[str, Union[str, datetime, bool]]

    def __init__(self, habit_repository: HabitRepository) -> None:
        self._habit_repository = habit_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def execute(self, input_data: InputData) -> OutputData:
        self._logger.info(
            "Retrieving habits in time frame from %s to %s",
            input_data.start_date,
            input_data.end_date,
        )
        habits = self._habit_repository.get_habits_in_time_frame(
            start_date=input_data.start_date, end_date=input_data.end_date
        )

        self._logger.info("Retrieved %d habits", len(habits))

        # Transform habits to a dictionary format suitable for output
        habits_dict = {
            habit.id: {
                "name": habit.name,
            }
            for habit in habits
        }

        return self.OutputData(habits=habits_dict)
