from fastapi import FastAPI
from fastapi.testclient import TestClient

from pebble.infrastructure.api.routes.habits import habit_router

# Create a FastAPI app and include the router for testing
app = FastAPI()
app.include_router(habit_router, prefix="/habits")

client = TestClient(app)


def test_create_habit() -> None:
    # Arrange
    request_data = {
        "name": "Test Habit",
        "recurrence": "daily",
        "description": "A test habit",
        "category_id": "123",
        "color_hex": "#FFFFFF",
    }

    # Act
    response = client.post("/habits/", json=request_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == {
        "message": "Habit created successfully",
        "habit": "Test Habit",
    }


def test_get_habit_by_id() -> None:
    # Arrange
    habit_id = "test-id"

    # Act
    response = client.get(f"/habits/{habit_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": habit_id,
        "name": "Sample Habit",
        "description": "This is a sample habit description.",
        "is_active": True,
        "created_at": response.json()["created_at"],  # Validate dynamic timestamp
    }
