from datetime import datetime

from pydantic import BaseModel


class HabitResponse(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
