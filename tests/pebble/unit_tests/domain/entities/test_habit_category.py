from pebble.domain.entities import HabitCategory
from pebble.domain.value_objects import Color


def test_create_habit_category():
    category = HabitCategory(name="Test Category", description="Test description")
    assert category.name == "Test Category"
    assert category.description == "Test description"
    assert category.color is None
    assert category.id is None


def test_create_habit_category_with_color():
    color = Color(hex="#FFFFFF")
    category = HabitCategory(
        name="Test Category", description="Test description", color=color
    )
    assert category.name == "Test Category"
    assert category.description == "Test description"
    assert category.color == color
    assert category.id is None


def test_create_habit_category_with_id():
    category = HabitCategory(name="Test Category", description="Test description", id=1)
    assert category.name == "Test Category"
    assert category.description == "Test description"
    assert category.color is None
    assert category.id == 1


def test_habit_category_equality_without_id():
    category1 = HabitCategory(name="Test Category", description="Test description")
    category2 = HabitCategory(name="Test Category", description="Test description")
    assert category1 == category2


def test_habit_category_inequality_without_id():
    category1 = HabitCategory(name="Test Category", description="Test description")
    category2 = HabitCategory(
        name="Another Category", description="Another description"
    )
    assert category1 != category2


def test_habit_category_equality_with_id():
    category1 = HabitCategory(
        name="Test Category", description="Test description", id=1
    )
    category2 = HabitCategory(
        name="Another Category", description="Another description", id=1
    )
    assert category1 == category2


def test_habit_category_inequality_with_different_id():
    category1 = HabitCategory(
        name="Test Category", description="Test description", id=1
    )
    category2 = HabitCategory(
        name="Test Category", description="Test description", id=2
    )
    assert category1 != category2


def test_habit_category_equality_with_color():
    color = Color(hex="#FFFFFF")
    category1 = HabitCategory(
        name="Test Category", description="Test description", color=color
    )
    category2 = HabitCategory(
        name="Test Category", description="Test description", color=color
    )
    assert category1 == category2


def test_habit_category_inequality_with_different_color():
    color1 = Color(hex="#FFFFFF")
    color2 = Color(hex="#000000")
    category1 = HabitCategory(
        name="Test Category", description="Test description", color=color1
    )
    category2 = HabitCategory(
        name="Test Category", description="Test description", color=color2
    )
    assert category1 != category2


def test_habit_category_inequality_with_different_name():
    category1 = HabitCategory(name="Test Category", description="Test description")
    category2 = HabitCategory(name="Another Category", description="Test description")
    assert category1 != category2


def test_habit_category_inequality_with_different_description():
    category1 = HabitCategory(name="Test Category", description="Test description")
    category2 = HabitCategory(name="Test Category", description="Another description")
    assert category1 != category2


def test_habit_category_equality_with_all_attributes():
    color = Color(hex="#FFFFFF")
    category1 = HabitCategory(
        name="Test Category", description="Test description", color=color, id=1
    )
    category2 = HabitCategory(
        name="Test Category", description="Test description", color=color, id=1
    )
    assert category1 == category2


def test_habit_category_inequality_with_different_all_attributes():
    color1 = Color(hex="#FFFFFF")
    color2 = Color(hex="#000000")
    category1 = HabitCategory(
        name="Test Category", description="Test description", color=color1, id=1
    )
    category2 = HabitCategory(
        name="Another Category", description="Another description", color=color2, id=2
    )
    assert category1 != category2
