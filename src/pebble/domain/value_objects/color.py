from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Color:
    hex: str
    name: str

    def __eq__(self, other: Color) -> bool:
        return self.hex == other.hex and self.name == other.name
