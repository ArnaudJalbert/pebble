from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, Union

from pebble.application.serializers.kv_serializer import KVSerializer
from pebble.domain.entities import HabitCategory
from pebble.domain.value_objects import Color


class HabitCategoryKVSerializer(KVSerializer):
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
        COLOR_HEX: ClassVar[str] = "color_hex"
        ID: ClassVar[str] = "_id"

    @classmethod
    def to_dict(cls, habit_category: HabitCategory) -> dict:
        data = {
            cls.DataKeys.NAME: habit_category.name,
            cls.DataKeys.DESCRIPTION: habit_category.description,
            cls.DataKeys.COLOR_HEX: habit_category.color.hex
            if habit_category.color
            else None,
        }

        if habit_category.id:
            data[cls.DataKeys.ID] = habit_category.id

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> HabitCategory:
        """
        Converts a dictionary representation of a habit category
        to a HabitCategory object.

        Args:
            data: The dictionary representation of the habit category.

        Returns:
            A HabitCategory object.
        """
        return HabitCategory(
            name=data[cls.DataKeys.NAME],
            description=data[cls.DataKeys.DESCRIPTION],
            color=Color(data[cls.DataKeys.COLOR_HEX]),
            id=str(data[cls.DataKeys.ID]) if cls.DataKeys.ID in data else None,
        )
