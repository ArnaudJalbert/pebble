import pytest
from mock_repository import MockRepository
from pebble.application.use_cases import CreateHabitCategory, CreateHabitCategoryDTO
from pebble.domain.entities import HabitCategory


@pytest.fixture
def habit_repository() -> MockRepository:
    return MockRepository()


def test_create_habit_category(habit_repository: MockRepository):
    use_case = CreateHabitCategory(habit_repository)
    dto = CreateHabitCategoryDTO(
        name="Cooking",
        description="Cooking meals at home",
        color="#FF0000",
    )
    habit_category: HabitCategory = use_case.execute(dto)

    # check that the habit category was saved to the repository
    assert len(habit_repository.save_habit_category_calls) == 1
    assert habit_repository.save_habit_category_calls[0].args[0] == habit_category

    assert habit_category.id is not None

    assert habit_category.name == "Cooking"
    assert habit_category.description == "Cooking meals at home"
    assert habit_category.color.hex == "#FF0000"


def test_create_habit_category_no_color(habit_repository: MockRepository):
    use_case = CreateHabitCategory(habit_repository)
    dto = CreateHabitCategoryDTO(
        name="Cooking",
        description="Cooking meals at home",
        color=None,
    )
    habit_category: HabitCategory = use_case.execute(dto)

    # check that the habit category was saved to the repository
    assert len(habit_repository.save_habit_category_calls) == 1
    assert habit_repository.save_habit_category_calls[0].args[0] == habit_category

    assert habit_category.id is not None

    assert habit_category.name == "Cooking"
    assert habit_category.description == "Cooking meals at home"
    assert habit_category.color is None


def test_create_habit_category_no_description(habit_repository: MockRepository):
    use_case = CreateHabitCategory(habit_repository)
    dto = CreateHabitCategoryDTO(
        name="Cooking",
        description=None,
        color="#FF0000",
    )
    habit_category: HabitCategory = use_case.execute(dto)

    # check that the habit category was saved to the repository
    assert len(habit_repository.save_habit_category_calls) == 1
    assert habit_repository.save_habit_category_calls[0].args[0] == habit_category

    assert habit_category.id is not None

    assert habit_category.name == "Cooking"
    assert habit_category.description is None
    assert habit_category.color.hex == "#FF0000"


def test_create_habit_category_no_description_or_color(
    habit_repository: MockRepository,
):
    use_case = CreateHabitCategory(habit_repository)
    dto = CreateHabitCategoryDTO(
        name="Cooking",
        description=None,
        color=None,
    )
    habit_category: HabitCategory = use_case.execute(dto)

    # check that the habit category was saved to the repository
    assert len(habit_repository.save_habit_category_calls) == 1
    assert habit_repository.save_habit_category_calls[0].args[0] == habit_category

    assert habit_category.id is not None

    assert habit_category.name == "Cooking"
    assert habit_category.description is None
    assert habit_category.color is None
