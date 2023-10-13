"""Represent a 2D vector."""

from __future__ import annotations  # self-referential type annotations

import math


class Vector:
    """Currently 2D, soon to be arbitrary dimensions."""

    def __init__(self, x: float, y: float) -> None:
        """Build vector from coordinates."""
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Official string representation."""
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r})"

    def __str__(self) -> str:
        """Show the coords."""
        return f"({self.x!r}, {self.y!r})"

    def __abs__(self) -> float:
        """Length of line from origin to point."""
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        """True for non-origin vectors."""
        return bool(abs(self))

    def __add__(self, other: Vector) -> Vector:
        """Addition of two Vectors."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other: Vector) -> Vector:
        """Subtraction of two Vectors."""
        x: float = self.x - other.x
        y: float = self.y - other.y
        return Vector(x, y)

    def __mul__(self, scalar: float) -> Vector:
        """Multiply Vector by a scalar."""
        return Vector(self.x * scalar, self.y * scalar)

    # avoid problem with Liskov substitution principle by
    # using "object" instead of Vector
    def __eq__(self, other: object) -> bool:
        """Fuzzy comparison of two Vectors."""
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.x, other.x, rel_tol=1e-6) and math.isclose(
            self.y, other.y, rel_tol=1e-6
        )

    def __hash__(self) -> int:
        """Create hash of Vector."""
        return hash((self.x, self.y))

    def rotate_90(self) -> Vector:
        """Rotate a vector by 90 degrees."""
        return Vector(self.y, -self.x)

    def normalize(self) -> Vector:
        """Normalize a vector."""
        # division by scalar not defined, so multiply by reciprocal
        return self * (1.0 / abs(self))
