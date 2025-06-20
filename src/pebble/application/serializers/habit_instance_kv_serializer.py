from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import ClassVar

from pebble.application.serializers.kv_serializer import KVSerializer
from pebble.domain.entities import Habit, HabitInstance


class HabitInstanceKVSerializer(KVSerializer):
    """
    Class to serialize a HabitInstance object.

    Contains the class DataKeys which defines
    the keys used to access the habit instance data.

    The to_dict method is used to convert the HabitInstance object
    to a dictionary representation.
    """

    @dataclass(frozen=True)
    class DataKeys:
        """
        This class contains the keys used to access the habit instance data.

        Attributes
            HABIT_ID: The key for the ID of the habit associated with the instance.
            DATE: The key for the date of the habit instance.
            ID: The key for the ID of the habit instance.
        """

        HABIT_ID: ClassVar[str] = "habit_id"
        DATE: ClassVar[str] = "date"
        COMPLETED: ClassVar[str] = "completed"
        NOTE: ClassVar[str] = "note"
        ID: ClassVar[str] = "_id"

    @classmethod
    def to_dict(cls, habit_instance: HabitInstance) -> dict:
        """
        Converts the habit instance to a dictionary representation.

        This is useful for serialization and storage in a database.

        Returns:
            The dictionary representation of the habit instance.
        """
        data = {
            cls.DataKeys.HABIT_ID: str(habit_instance.habit.id),
            cls.DataKeys.DATE: habit_instance.date.isoformat(),
            cls.DataKeys.COMPLETED: habit_instance.completed,
            cls.DataKeys.NOTE: habit_instance.note,
        }

        if habit_instance.id:
            data[cls.DataKeys.ID] = str(habit_instance.id)

        return data

    @classmethod
    def from_dict(cls, data: dict, habit: Habit) -> HabitInstance:
        """
        Converts a dictionary representation back to a HabitInstance object.

        Args:
            data: The dictionary representation of the habit instance.
            habit: The Habit object associated with this instance.

        Returns:
            A HabitInstance object created from the dictionary data.
        """
        habit_instance_id = data.get(cls.DataKeys.ID)
        return HabitInstance(
            id=str(habit_instance_id) if habit_instance_id else None,
            habit=habit,
            date=datetime.date.fromisoformat(data[cls.DataKeys.DATE]),
            completed=data[cls.DataKeys.COMPLETED],
            note=data.get(cls.DataKeys.NOTE, ""),
        )
