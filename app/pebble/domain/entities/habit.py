from datetime import datetime
from typing import Type, Optional

from pydantic import BaseModel

from .recurrence import Recurrence


class Habit(BaseModel):
    """
    Habit Entity that represents a habit that a user wants to track.

    Attributes:
        name: The name of the habit.
        recurrence: The recurrence of the habit, for example daily, weekly, monthly...
        description: The description of the habit.
        id: The unique identifier of the habit.
        user_id: The unique identifier of the user that owns the habit.
        created_at: The datetime when the habit was created.
        updated_at: The datetime when the habit was last updated
    """

    name: str
    recurrence: Type[Recurrence]
    description: Optional[str] = None

    id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
