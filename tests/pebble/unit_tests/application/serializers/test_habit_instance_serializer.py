import datetime

from pebble.application.serializers.habit_instance_kv_serializer import (
    HabitInstanceKVSerializer,
)
from pebble.domain.entities.habit import Habit
from pebble.domain.entities.habit_instance import HabitInstance
from pebble.domain.value_objects.types import ID, Name


def test_habit_instance_kv_serializer() -> None:
    # Create a sample Habit object
    habit = Habit(name=Name("Drink Water"), recurrence=None, id=ID("habit1"))

    # Create a HabitInstance object
    habit_instance = HabitInstance(
        habit=habit,
        date=datetime.date(2023, 10, 1),
        completed=True,
        note="Completed successfully",
        id=ID("instance1"),
    )

    # Serialize the HabitInstance object
    serialized_data = HabitInstanceKVSerializer.to_dict(habit_instance)

    # Assert the serialized data
    assert serialized_data == {
        "habit_id": "habit1",
        "date": "2023-10-01",
        "completed": True,
        "note": "Completed successfully",
        "_id": "instance1",
    }

    # Deserialize the data back into a HabitInstance object
    deserialized_instance = HabitInstanceKVSerializer.from_dict(
        serialized_data,
        habit=habit,
    )

    # Assert the deserialized object matches the original
    assert deserialized_instance == habit_instance
