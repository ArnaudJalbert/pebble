"""
General types for value objects.
"""

from typing import Annotated

Name = Annotated[str, "Name of the object, must be less than 255 characters."]
Description = Annotated[
    str, "Description of the object, must be less than 255 characters."
]
ID = Annotated[int, "The ID of the object, must be unique and greater than 0."]
Note = Annotated[str, "Note of the object, must be less than 255 characters."]
