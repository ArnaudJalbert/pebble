"""
General types for value objects.
"""

from typing import Annotated

Name = Annotated[str, "Name of the object, must be less than 255 characters."]

Username = Annotated[
    str, "String that represents a username, must be less than 255 characters."
]

Email = Annotated[
    str, "String that represents an email address, must be in a valid email format."
]

Description = Annotated[str, "String that represents a description."]

ID = Annotated[str, "The ID of the object, it is a unique string."]

Note = Annotated[str, "A string that represents a note."]
