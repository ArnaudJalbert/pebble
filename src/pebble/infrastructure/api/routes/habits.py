import logging
from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from pebble.infrastructure.api.models.habit import CreateHabitRequest, HabitResponse

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

habit_router = APIRouter()


@habit_router.get("/{habit_id}")
def get_habit_by_id(habit_id: str) -> HabitResponse:
    return HabitResponse(
        id=habit_id,
        name="Sample Habit",
        description="This is a sample habit description.",
        is_active=True,
        created_at=datetime.now(),
    )


@habit_router.post("/")
def create_habit(request: CreateHabitRequest) -> JSONResponse:
    """
    Creates a new habit in persistent storage.
    This endpoint allows users to create a new habit by providing the necessary details
    such as name, recurrence, and optional fields like description, category ID,
    and color hex.

    Args:
        request: The request body containing the details of the habit to be created,
        the format of the request body is defined by the CreateHabitRequest model.

    Returns:
        The response indicating the success of the operation.
    """
    # TODO -> Implement the logic to create a habit in the repository.

    logger.info(
        f"Creating habit with name: {request.name}, recurrence: {request.recurrence}"
    )

    return JSONResponse(
        content={"message": "Habit created successfully", "habit": request.name},
        status_code=status.HTTP_201_CREATED,
    )
