from datetime import datetime
from unittest.mock import MagicMock

from pebble.application.use_cases.retrieve_habits_in_time_frame import (
    RetrieveHabitsInTimeFrame,
)
from pebble.domain.entities.habit import Habit


def test_retrieve_habits_in_time_frame() -> None:
    # Arrange
    mock_habit_repository = MagicMock()
    mock_habit_repository.get_habits_in_time_frame.return_value = [
        Habit(
            id="1",
            name="Habit 1",
            recurrence="daily",
            description="Description 1",
            category=None,
            color=None,
        ),
        Habit(
            id="2",
            name="Habit 2",
            recurrence="weekly",
            description="Description 2",
            category=None,
            color=None,
        ),
    ]

    use_case = RetrieveHabitsInTimeFrame(habit_repository=mock_habit_repository)
    input_data = RetrieveHabitsInTimeFrame.InputData(
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 1, 31),
    )

    # Act
    result = use_case.execute(input_data)

    # Assert
    mock_habit_repository.get_habits_in_time_frame.assert_called_once_with(
        start_date=input_data.start_date, end_date=input_data.end_date
    )
    assert result.habits == {"1": {"name": "Habit 1"}, "2": {"name": "Habit 2"}}
