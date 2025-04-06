from dataclasses import dataclass
from typing import Any, List, Union

from pebble.application.repositories import HabitRepository
from pebble.domain.entities import Habit, HabitCategory, HabitCollection, HabitInstance
from pebble.domain.value_objects.types import ID


@dataclass
class Call:
    args: List
    return_value: Any


class MockRepository(HabitRepository):
    def __init__(self) -> None:
        self.habits = []
        self.categories = []
        self.habit_collections = []
        self.habit_instances = []

        self.save_habit_calls = []
        self.save_habit_category_calls = []
        self.get_category_by_name_calls = []
        self.get_habits_by_ids_calls = []
        self.save_habit_collection_calls = []
        self.get_habit_by_id_calls = []
        self.save_habit_instances_calls = []
        self.get_habit_collection_by_id_calls = []
        self.update_habit_collection_calls = []

    def save_habit(self, habit: Habit) -> Habit:
        habit.id = ID(len(self.habits) + 1)
        self.habits.append(habit)

        self.save_habit_calls.append(Call(args=[habit], return_value=habit))

        return habit

    def get_habits_by_ids(self, habits_ids: set[ID]) -> set[Habit]:
        habits = {habit for habit in self.habits if habit.id in habits_ids}

        self.get_habits_by_ids_calls.append(Call(args=[habits], return_value=habits))

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

    def get_habit_collection_by_id(self, habit_collection_id: ID) -> HabitCollection:
        habit_collection_to_return = None
        for habit_collection in self.habit_collections:
            if habit_collection.id == habit_collection_id:
                habit_collection_to_return = habit_collection
                break

        self.get_habit_collection_by_id_calls.append(
            Call(args=[habit_collection_id], return_value=habit_collection_to_return)
        )

        return habit_collection_to_return

    def get_habit_by_id(self, habit_id: ID) -> Habit:
        habit_to_return = None
        for habit in self.habits:
            if habit.id == habit_id:
                habit_to_return = habit
                break
        self.get_habit_by_id_calls.append(
            Call(args=[habit_id], return_value=habit_to_return)
        )
        return habit_to_return

    def save_habit_instance(self, habit_instance: HabitInstance) -> HabitInstance:
        habit_instance.id = ID(str(len(self.habit_instances) + 1))
        self.habit_instances.append(habit_instance)

        self.save_habit_instances_calls.append(
            Call(args=[habit_instance], return_value=habit_instance)
        )

        return habit_instance

    def update_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        for i, hc in enumerate(self.habit_collections):
            if hc.id == habit_collection.id:
                self.habit_collections[i] = habit_collection
                break

        self.update_habit_collection_calls.append(
            Call(args=[habit_collection], return_value=habit_collection)
        )

        return habit_collection
