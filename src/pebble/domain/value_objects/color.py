from __future__ import annotations

import re
from dataclasses import dataclass


class InvalidColorFormatError(Exception):
    """Raised when the color format is invalid."""


HEX_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


@dataclass
class Color:
    hex: str

    def __post_init__(self):
        if not self.is_valid_hex(self.hex):
            raise InvalidColorFormatError("Invalid color format")

    def __eq__(self, other: Color) -> bool:
        return self.hex == other.hex

    @staticmethod
    def is_valid_hex(hex_str: str) -> bool:
        """
        Validates if the given string is a valid hexadecimal color code.

        Args:
            hex_str: The string to validate.

        Returns:
            True if the string is a valid hexadecimal color code, False otherwise.
        """
        return bool(HEX_PATTERN.match(hex_str))
