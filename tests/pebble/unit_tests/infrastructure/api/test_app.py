from fastapi.testclient import TestClient

from pebble.infrastructure.api.app import app

client = TestClient(app)

def test_health_check() -> None:
    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_habit_by_id() -> None:
    # Arrange
    habit_id = "test-id"

    # Act
    response = client.get(f"/habit/{habit_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": habit_id,
        "name": "Sample Habit",
        "description": "This is a sample habit description.",
        "is_active": True,
        "created_at": response.json()["created_at"],  # Validate dynamic timestamp
    }

def test_create_habit() -> None:
    # Arrange
    request_data = {
        "name": "Test Habit",
        "recurrence": "daily",
        "description": "A test habit",
        "category_id": "123",
        "color_hex": "#FFFFFF"
    }

    # Act
    response = client.post("/habit/", json=request_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == {
        "message": "Habit created successfully",
        "habit": "Test Habit"
    }