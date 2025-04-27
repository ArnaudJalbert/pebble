from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar


class KVSerializer(ABC):
    """
    Abstract class to serialize an object to a dictionary representation.

    This class is intended to be subclassed by specific serializers.

    The to_dict method must be implemented by subclasses to convert the object
    to a dictionary representation.

    Implemented as a singleton to ensure that only one instance exists.

    Attributes:
        _instance: The singleton instance of HabitSerializer.
    """

    _instance: ClassVar[KVSerializer] = None

    def __new__(cls) -> KVSerializer:
        """
        Create a new instance of HabitSerializer.

        If an instance already exists, return the existing instance.

        This is to ensure that the HabitSerializer is a singleton.

        Returns:
            The singleton instance of HabitSerializer.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    @abstractmethod
    def to_dict(cls, obj: object) -> dict:
        """
        Converts the object to a dictionary representation.

        Args:
            obj: The object to convert.

        Returns:
            The dictionary representation of the object.
        """
