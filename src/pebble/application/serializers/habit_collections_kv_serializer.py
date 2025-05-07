from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, List, Set, Union

from pebble.application.serializers.kv_serializer import KVSerializer
from pebble.domain.entities import Habit, HabitCollection, HabitInstance
from pebble.domain.value_objects import ID


class HabitCollectionsKVSerializer(KVSerializer):
    """
    This class is responsible for serializing and deserializing
    HabitCategory objects to and from a key-value format.

    It provides methods to convert a HabitCategory object to a dictionary
    and to create a HabitCategory object from a dictionary.
    """

    @dataclass(frozen=True)
    class DataKeys:
        """
        This class contains the keys used to access the habit data.

        Attributes
            NAME: The key for the name of the habit.
            RECURRENCE: The key for the recurrence of the habit.
            RECURRENCE_DAYS: The key for the days of the week for the habit.
            DESCRIPTION: The key for the description of the habit.
            CATEGORY_ID: The key for the category ID of the habit.
            COLOR_HEX: The key for the color hex code of the habit.
            ID: The key for the ID of the habit.
        """

        NAME: ClassVar[str] = "name"
        DESCRIPTION: ClassVar[str] = "description"
        HABITS: ClassVar[str] = "habits"
        HABITS_INSTANCES: ClassVar[str] = "habits_instances"
        ID: ClassVar[str] = "_id"

    @classmethod
    def to_dict(cls, habit_collection: HabitCollection) -> dict:
        """
        Converts a HabitCollection object to a dictionary.

        This method is used to serialize the HabitCollection object
        to a key-value format.

        The habits and habits_instances attributes are converted to a list of IDs.
        The ID attribute is included if it exists.

        Args:
            habit_collection: The HabitCollection object to be serialized.

        Returns:
            The serialized HabitCollection object as a dictionary.
        """
        data = {
            cls.DataKeys.NAME: habit_collection.name,
            cls.DataKeys.DESCRIPTION: habit_collection.description,
            cls.DataKeys.HABITS: [h.id for h in habit_collection.habits],
            cls.DataKeys.HABITS_INSTANCES: [
                h.id for h in habit_collection.habits_instance
            ],
        }

        if habit_collection.id:
            data[cls.DataKeys.ID] = habit_collection.id

        return data

    @classmethod
    def from_dict(
        cls,
        habit_collection_data: Dict[
            str,
            Union[str, List[ID]],
        ],
        habits: Set[Habit],
        habits_instances: Set[HabitInstance],
    ) -> HabitCollection:
        """
        Converts a dictionary to a HabitCollection object.

        This method is used to deserialize the dictionary
        to a HabitCollection object.

        The habits and habits_instances need to be provided and deserialized
        separately, as they are not included in the dictionary.

        Args:
            habit_collection_data: The dictionary containing the habit collection data.
            habits: A set of Habit objects that belong to the collection.
            habits_instances: A set of HabitInstance objects that belong to
            the collection.

        Returns:
            The deserialized HabitCollection object.
        """
        return HabitCollection(
            name=habit_collection_data[cls.DataKeys.NAME],
            description=habit_collection_data.get(cls.DataKeys.DESCRIPTION),
            habits=habits,
            habits_instance=habits_instances,
            id=habit_collection_data.get(cls.DataKeys.ID),
        )
