import pytest

from pebble.domain.entities.habit import Habit
from pebble.domain.entities.habit_collection import HabitCollection
from pebble.domain.value_objects.types import Name


def test_add_habit_to_collection_raises_value_error_when_habit_exists() -> None:
    # Initialize the HabitCollection with a valid Name object
    habit_collection = HabitCollection(name=Name("Daily Habits"))
    habit = Habit(name=Name("Drink Water"), recurrence=None)

    # Add the habit to the collection
    habit_collection.add_habit(habit)

    # Attempt to add the same habit again, expecting a ValueError
    with pytest.raises(
        ValueError, match="Habit Drink Water already exists in the collection"
    ):
        habit_collection.add_habit(habit)
