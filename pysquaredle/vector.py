"""
Represent a 2D vector
"""

from __future__ import annotations  # self-referential type annotations

import math


class Vector:
    """
    Currently 2D, soon to be arbitrary dimensions
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r})"

    def __str__(self) -> str:
        return f"({self.x!r}, {self.y!r})"

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __add__(self, other: Vector) -> Vector:
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other: Vector) -> Vector:
        x: float = self.x - other.x
        y: float = self.y - other.y
        return Vector(x, y)

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)

    # avoid problem with Liskov substitution principle by using "object" instead of Vector
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.x, other.x, rel_tol=1e-6) and math.isclose(
            self.y, other.y, rel_tol=1e-6
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def rotate_90(self) -> Vector:
        """
        Rotate a vector by 90 degrees
        """
        return Vector(self.y, -self.x)

    def normalize(self) -> Vector:
        """
        Normalize a vector
        """
        # division by scalar not defined, so multiply by reciprocal
        return self * (1.0 / abs(self))
