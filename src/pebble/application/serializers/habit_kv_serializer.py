from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from pebble.application.serializers.kv_serializer import KVSerializer
from pebble.domain.entities import Habit


class HabitKVSerializer(KVSerializer):
    """
    Class to serialize a Habit object.

    Contains the class DataKeys which defines the keys used to access the habit data.

    The to_dict method is used to convert the Habit object
    to a dictionary representation.

    Converts the Habit object to a dictionary representation.
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
        RECURRENCE: ClassVar[str] = "recurrence"
        RECURRENCE_DAYS: ClassVar[str] = "recurrence_days"
        DESCRIPTION: ClassVar[str] = "description"
        CATEGORY_ID: ClassVar[str] = "category_id"
        COLOR_HEX: ClassVar[str] = "color_hex"
        ID: ClassVar[str] = "_id"

    @classmethod
    def to_dict(cls, habit: Habit) -> dict[str, str | int | list[str] | None]:
        """
        Converts the habit to a dictionary representation.

        This is useful for serialization and storage in a database.

        The object that are also stored in the database are simply represented by id.

        Returns:
            The dictionary representation of the habit.
        """
        data = {
            cls.DataKeys.NAME: habit.name,
            cls.DataKeys.RECURRENCE: habit.recurrence.name,
            cls.DataKeys.RECURRENCE_DAYS: [
                d.value for d in habit.recurrence.days_of_week
            ],
            cls.DataKeys.DESCRIPTION: habit.description,
            cls.DataKeys.CATEGORY_ID: habit.category.id if habit.category else None,
            cls.DataKeys.COLOR_HEX: habit.color.hex if habit.color else None,
        }

        if habit.id:
            data[cls.DataKeys.ID] = habit.id

        return data
