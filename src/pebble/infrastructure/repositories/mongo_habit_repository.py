from typing import Set, Union

from pymongo import MongoClient

from pebble.application.repositories import HabitRepository
from pebble.domain.entities import Habit, HabitCategory, HabitCollection, HabitInstance
from pebble.domain.value_objects import ID


class MongoHabitRepository(HabitRepository):
    def __init__(self, mongo_client: MongoClient) -> None:
        self.mongo_client = mongo_client

    def save_habit(self, habit: Habit) -> Habit:
        pass

    def get_habit_by_id(self, habit_id: str) -> Habit:
        pass

    def get_habits_by_ids(self, habits_ids: Set[ID]) -> Set[Habit]:
        pass

    def save_habit_category(self, habit_category: HabitCategory) -> HabitCategory:
        pass

    def get_habit_category_by_name(
        self, category_name: str
    ) -> Union[HabitCategory, None]:
        pass

    def save_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        pass

    def update_habit_collection(
        self, habit_collection: HabitCollection
    ) -> HabitCollection:
        pass

    def get_habit_collection_by_id(self, habit_collection_id: ID) -> HabitCollection:
        pass

    def save_habit_instance(self, habit_instance: HabitInstance) -> HabitInstance:
        pass
