import pytest

from pebble.domain.value_objects import Color
from pebble.domain.value_objects.color import InvalidColorFormatError


def test_invalid_color():
    with pytest.raises(InvalidColorFormatError):
        Color("invalid color")
