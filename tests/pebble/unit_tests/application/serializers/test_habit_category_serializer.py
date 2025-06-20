from pebble.application.serializers import HabitCategoryKVSerializer
from pebble.domain.entities import HabitCategory
from pebble.domain.value_objects import Color


def test_habit_category_serializer_from_dict() -> None:
    """
    Test the HabitCategorySerializer's from_dict method.
    """

    # Create a dictionary representing a habit category
    category_data = {
        HabitCategoryKVSerializer.DataKeys.NAME: "Test Category",
        HabitCategoryKVSerializer.DataKeys.DESCRIPTION: "This is a test category",
        HabitCategoryKVSerializer.DataKeys.COLOR_HEX: "#FF5733",
        HabitCategoryKVSerializer.DataKeys.ID: "123456",
    }

    # Deserialize the dictionary into a HabitCategory object
    serializer = HabitCategoryKVSerializer()
    category = serializer.from_dict(category_data)

    # Check that the deserialized object matches the expected values
    assert category.name == category_data[HabitCategoryKVSerializer.DataKeys.NAME]
    assert (
        category.description
        == category_data[HabitCategoryKVSerializer.DataKeys.DESCRIPTION]
    )
    assert (
        category.color.hex
        == category_data[HabitCategoryKVSerializer.DataKeys.COLOR_HEX]
    )
    assert category.id == category_data[HabitCategoryKVSerializer.DataKeys.ID]


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
