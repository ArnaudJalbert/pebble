from pebble.application.serializers import HabitCategoryKVSerializer
from pebble.domain.entities import HabitCategory
from pebble.domain.value_objects import Color


def test_habit_category_serializer() -> None:
    """
    Test the HabitCategorySerializer class.
    """

    # Create a habit category object
    category = HabitCategory(
        name="Test Category",
        description="This is a test category",
        color=Color(hex="#FF5733"),
    )

    # Serialize the habit category object
    serializer = HabitCategoryKVSerializer()
    serialized_category = serializer.to_dict(category)

    # Check that the serialized data matches the expected format
    assert serialized_category[serializer.DataKeys.NAME] == category.name
    assert serialized_category[serializer.DataKeys.DESCRIPTION] == category.description
    assert serialized_category[serializer.DataKeys.COLOR_HEX] == category.color.hex
    assert serialized_category.get(serializer.DataKeys.ID) is None


def test_habit_category_serializer_with_id() -> None:
    """
    Test the HabitCategorySerializer class with an ID.
    """

    # Create a habit category object
    category = HabitCategory(
        name="Test Category",
        description="This is a test category",
        color=Color(hex="#FF5733"),
        id="123456",
    )

    # Serialize the habit category object
    serializer = HabitCategoryKVSerializer()
    serialized_category = serializer.to_dict(category)

    # Check that the serialized data matches the expected format
    assert serialized_category[serializer.DataKeys.NAME] == category.name
    assert serialized_category[serializer.DataKeys.DESCRIPTION] == category.description
    assert serialized_category[serializer.DataKeys.COLOR_HEX] == category.color.hex
    assert serialized_category[serializer.DataKeys.ID] == category.id
