from dataclasses import dataclass
from typing import Optional, Union

from pebble.application.factories import RecurrenceFactory
from pebble.application.repositories.habits_repository import HabitRepository
from pebble.domain.entities import Habit, HabitCategory
from pebble.domain.entities.recurrences import Recurrence
from pebble.domain.value_objects import Color


@dataclass(frozen=True)
class CreateNewHabitDTO:
    name: str
    recurrence: str
    description: Optional[str] = None
    category_name: Optional[str] = None
    category_color: Optional[str] = None
    category_description: Optional[str] = None
    recurrence_days: Optional[set[str]] = None
    habit_color: Optional[str] = None


class CreateNewHabit:
    """
    Use case to create a new habit entity.
    The use case will create a new habit entity based on the data provided in the DTO.
    It is responsible for creating a new habit entity, creating a new habit category if it does not exist,
    and creating a new recurrence object based on the data provided in the DTO.
    The use case will save the habit entity to the habit repository and return the habit entity with a unique identifier.

    Attributes:
        habit_repository: The repository used to save the habit
    """

    def __init__(self, habit_repository: HabitRepository) -> None:
        """
        Initializes the CreateNewHabit use case with the habit repository.

        Args:
            habit_repository: The repository used to access the data layer.
        """
        self.habit_repository: HabitRepository = habit_repository

    def execute(self, dto: CreateNewHabitDTO) -> Habit:

        # create a recurrence object, there must be a recurrence provided
        recurrence: Recurrence = self._create_recurrence(dto)

        # set the color to None if it is not provided, else create a Color object
        color: Union[Color, None] = (
            Color(hex=dto.habit_color) if dto.habit_color else None
        )

        # create a habit category object
        habit_category: Union[HabitCategory, None] = (
            self._create_habit_category(dto) if dto.category_name else None
        )

        # create a new habit entity
        habit: Habit = Habit(
            name=dto.name,
            description=dto.description,
            recurrence=recurrence,
            category=habit_category,
            color=color,
        )

        # save the habit to the repository, this will assign a unique identifier to the habit
        return self.habit_repository.save_habit(habit)

    def _create_habit_category(self, dto):
        # get the category by name if it exists
        habit_category = self.habit_repository.get_category_by_name(dto.category_name)

        # if the category does not exist, create a new one
        if not habit_category:
            habit_category: HabitCategory = HabitCategory(
                name=dto.category_name,
                description=dto.category_description,
                color=Color(hex=dto.category_color) if dto.category_color else None,
            )
            habit_category = self.habit_repository.save_habit_category(habit_category)

        return habit_category

    @staticmethod
    def _create_recurrence(dto):
        # find the recurrence class based on the name provided in the DTO

        recurrence = RecurrenceFactory.get_recurrence_from_strings(
            dto.recurrence, dto.recurrence_days
        )

        return recurrence
