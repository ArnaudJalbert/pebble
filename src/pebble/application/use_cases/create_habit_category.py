from dataclasses import dataclass
from typing import Optional, Union

from pebble.application.repositories import HabitRepository
from pebble.domain.entities.habit_category import HabitCategory
from pebble.domain.value_objects import Color


@dataclass(frozen=True)
class CreateHabitCategoryDTO:
    name: str
    description: Optional[str]
    color: Optional[str]


class CreateHabitCategory:
    """
    Use case to create a new habit category entity.
    The use case will create a new habit category entity based on the data provided in the DTO.
    It is responsible for creating a new habit category entity and saving it to the habit category repository.

    Attributes:
        habit_category_repository: The repository used to save the habit category
    """

    def __init__(self, habit_category_repository: HabitRepository):
        """
        Initializes the CreateHabitCategory use case with the habit category repository.

        Args:
            habit_category_repository: The repository used to access the data layer.
        """
        self.habit_category_repository: HabitRepository = habit_category_repository

    def execute(self, dto: CreateHabitCategoryDTO) -> HabitCategory:
        """
        Creates a new habit category entity based on the data provided in the DTO.

        Args:
            dto: The data transfer object containing the data to create the habit category.

        Returns:
            The created habit category entity, with an ID.
        """
        color: Union[Color, None] = Color(dto.color) if dto.color else None

        habit_category = HabitCategory(
            name=dto.name,
            description=dto.description,
            color=color,
        )

        return self.habit_category_repository.save_habit_category(habit_category)
