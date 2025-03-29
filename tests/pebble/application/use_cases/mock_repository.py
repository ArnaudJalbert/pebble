from dataclasses import dataclass
from typing import Union, Any, List

from pebble.application.repositories import HabitRepository
from pebble.domain.entities import Habit, HabitCategory
from pebble.domain.value_objects.types import ID


@dataclass
class Call:
    args: List
    return_value: Any


class MockRepository(HabitRepository):
    def __init__(self):
        self.habits = []
        self.categories = []
        self.save_habit_calls = []
        self.save_habit_category_calls = []
        self.get_category_by_name_calls = []

    def save_habit(self, habit: Habit) -> Habit:
        habit.id = ID(str(len(self.habits) + 1))
        self.habits.append(habit)

        self.save_habit_calls.append(Call(args=[habit], return_value=habit))

        return habit

    def save_habit_category(self, habit_category: HabitCategory) -> HabitCategory:
        habit_category.id = ID(str(len(self.categories) + 1))
        self.categories.append(habit_category)

        self.save_habit_category_calls.append(
            Call(args=[habit_category], return_value=habit_category)
        )

        return habit_category

    def get_category_by_name(self, category_name: str) -> Union[HabitCategory, None]:
        habit_category = None
        for c in self.categories:
            if c.name == category_name:
                habit_category = c

        self.get_category_by_name_calls.append(
            Call(args=[category_name], return_value=habit_category)
        )

        return habit_category
