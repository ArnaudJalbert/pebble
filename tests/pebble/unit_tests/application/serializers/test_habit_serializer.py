from pebble.application.serializers import HabitKVSerializer
from pebble.domain.entities import Daily, Habit, HabitCategory
from pebble.domain.value_objects import Color


def test_habit_serializer() -> None:
    """
    Test the HabitSerializer class.
    """

    # Create a habit object
    habit = Habit(
        name="Test Habit",
        recurrence=Daily(),
        description="This is a test habit",
        category=HabitCategory(
            name="Test Category",
            description="This is a test category",
            color=Color(hex="#FF5733"),
            id="123456",
        ),
        color=Color(hex="#FF5733"),
    )

    # Serialize the habit object
    serializer = HabitKVSerializer()
    serialized_habit = serializer.to_dict(habit)

    # Check that the serialized data matches the expected format
    assert serialized_habit[serializer.DataKeys.NAME] == habit.name
    assert serialized_habit[serializer.DataKeys.RECURRENCE] == "Daily"
    assert len(serialized_habit[serializer.DataKeys.RECURRENCE_DAYS]) == 7
    for day in serialized_habit[serializer.DataKeys.RECURRENCE_DAYS]:
        assert day in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    assert serialized_habit[serializer.DataKeys.DESCRIPTION] == habit.description
    assert serialized_habit[serializer.DataKeys.CATEGORY_ID] == habit.category.id
    assert serialized_habit[serializer.DataKeys.COLOR_HEX] == habit.color.hex
    assert serialized_habit.get(serializer.DataKeys.ID) is None


def test_habit_serializer_with_id() -> None:
    """
    Test the HabitSerializer class with an ID.
    """

    # Create a habit object
    habit = Habit(
        name="Test Habit",
        recurrence=Daily(),
        description="This is a test habit",
        category=HabitCategory(
            name="Test Category",
            description="This is a test category",
            color=Color(hex="#FF5733"),
            id="123456",
        ),
        color=Color(hex="#FF5733"),
        id="1234567",
    )

    # Serialize the habit object
    serializer = HabitKVSerializer()
    serialized_habit = serializer.to_dict(habit)

    # Check that the serialized data matches the expected format
    assert serialized_habit[serializer.DataKeys.NAME] == habit.name
    assert serialized_habit[serializer.DataKeys.RECURRENCE] == "Daily"
    assert len(serialized_habit[serializer.DataKeys.RECURRENCE_DAYS]) == 7
    for day in serialized_habit[serializer.DataKeys.RECURRENCE_DAYS]:
        assert day in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    assert serialized_habit[serializer.DataKeys.DESCRIPTION] == habit.description
    assert serialized_habit[serializer.DataKeys.CATEGORY_ID] == habit.category.id
    assert serialized_habit[serializer.DataKeys.COLOR_HEX] == habit.color.hex
    assert serialized_habit[serializer.DataKeys.ID] == habit.id
