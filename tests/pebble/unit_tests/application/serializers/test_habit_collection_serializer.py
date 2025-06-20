# Python

from pebble.application.serializers.habit_collections_kv_serializer import (
    HabitCollectionsKVSerializer,
)
from pebble.domain.entities.habit import Habit
from pebble.domain.entities.habit_collection import HabitCollection
from pebble.domain.entities.habit_instance import HabitInstance
from pebble.domain.value_objects.types import ID, Description, Name


def test_habit_collections_kv_serializer() -> None:
    # Create sample Habit and HabitInstance objects
    habit = Habit(name=Name("Drink Water"), recurrence=None, id=ID("habit1"))
    habit_instance = HabitInstance(
        habit=habit, date=None, completed=True, id=ID("instance1")
    )

    # Create a HabitCollection object
    habit_collection = HabitCollection(
        name=Name("Daily Habits"),
        description=Description("A collection of daily habits"),
        habits={habit},
        habits_instance={habit_instance},
        id=ID("collection1"),
    )

    # Serialize the HabitCollection object
    serialized_data = HabitCollectionsKVSerializer.to_dict(habit_collection)

    # Assert the serialized data
    assert serialized_data == {
        "name": Name("Daily Habits"),
        "description": Description("A collection of daily habits"),
        "habits": ["habit1"],
        "habits_instances": ["instance1"],
        "_id": "collection1",
    }

    # Deserialize the data back into a HabitCollection object
    deserialized_collection = HabitCollectionsKVSerializer.from_dict(
        serialized_data,
        habits={habit},
        habits_instances={habit_instance},
    )

    # Assert the deserialized object matches the original
    assert deserialized_collection == habit_collection
