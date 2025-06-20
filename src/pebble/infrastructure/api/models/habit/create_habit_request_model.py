from typing import Optional

from pydantic import BaseModel


class CreateHabitRequest(BaseModel):
    name: str
    recurrence: str
    description: Optional[str] = None
    category_id: Optional[str] = None
    color_hex: Optional[str] = None
