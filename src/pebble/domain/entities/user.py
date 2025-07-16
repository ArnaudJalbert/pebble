from dataclasses import dataclass

from ..value_objects.types import ID, Email, Username


@dataclass(slots=True)
class User:
    """
    Represents a user in the system.

    Attributes:
        id: Unique identifier for the user.
        username: Username of the user.
        email: Email address of the user.
        is_active: Indicates if the user account is active.
    """

    id: ID
    username: Username
    email: Email

    is_active: bool = True
