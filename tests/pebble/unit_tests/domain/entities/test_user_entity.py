from pebble.domain.entities import User
from pebble.domain.value_objects.types import ID, Email, Username


def test_create_user() -> None:
    user = User(
        id=ID("123"),
        username=Username("testuser"),
        email=Email("testuser@example.com"),
    )
    assert user.id == ID("123")
    assert user.username == Username("testuser")
    assert user.email == Email("testuser@example.com")
    assert user.is_active
