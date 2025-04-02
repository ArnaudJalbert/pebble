from dataclasses import dataclass
from typing import Any, List, Union

from pebble.application.repositories import HabitRepository
from pebble.domain.entities import Habit, HabitCategory, HabitCollection
from pebble.domain.value_objects.types import ID


@dataclass
class Call:
    args: List
    return_value: Any


class MockRepository(HabitRepository):
    def __init__(self):
        self.habits = []
        self.categories = []
        self.habit_collections = []

        self.save_habit_calls = []
        self.save_habit_category_calls = []
        self.get_category_by_name_calls = []
        self.get_habits_by_ids_calls = []
        self.save_habit_collection_calls = []

    def save_habit(self, habit: Habit) -> Habit:
        habit.id = ID(len(self.habits) + 1)
        self.habits.append(habit)

        self.save_habit_calls.append(Call(args=[habit], return_value=habit))

        return habit

    def get_habits_by_ids(self, habits_ids: set[ID]) -> set[Habit]:
        habits = {habit for habit in self.habits if habit.id in habits_ids}

        self.get_habits_by_ids_calls.append(
            Call(args=[habits], return_value=habits)
        )

        return habits

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
                self.get_category_by_name_calls.append(
                    Call(args=[category_name], return_value=c)
                )
                return c

        self.get_category_by_name_calls.append(
            Call(args=[category_name], return_value=habit_category)
        )

        return habit_category

    def save_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        habit_collection.id = ID(str(len(self.habit_collections) + 1))
        self.habit_collections.append(habit_collection)

        self.save_habit_collection_calls.append(
            Call(args=[habit_collection], return_value=habit_collection)
        )

        return habit_collection
