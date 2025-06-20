from typing import Dict

import toml
from fastapi import FastAPI

from .routes import habit_router

app = FastAPI(
    version=toml.load("pyproject.toml")["project"]["version"],
)


@app.get("/health")
def health_check() -> Dict:
    """
    Health check endpoint to verify the service is running.
    This endpoint returns a simple JSON response indicating the service status.
    It is typically used by monitoring systems to check the health of the service.

    Returns:
        The health status of the service as a JSON object.
    """
    return {"status": "healthy"}


# Include the habit router for handling habit-related endpoints
app.include_router(habit_router, prefix="/habit", tags=["Habit"])
