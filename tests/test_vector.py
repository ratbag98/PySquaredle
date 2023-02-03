"""
Test my simple Vector class
"""

from math import isclose

import pytest

from pysquaredle.vector import Vector


def test_str() -> None:
    """
    Vector can be converted to a string
    """
    vec = Vector(2, 4)
    assert str(vec) == "(2, 4)"


def test_repr() -> None:
    """
    Vector can be converted to a string
    """
    vec = Vector(2, 4)
    assert repr(vec) == "Vector(2, 4)"


def test_addition() -> None:
    """
    Vector maths works
    """
    vec_1 = Vector(2, 4)
    vec_2 = Vector(2, 1)
    assert (vec_1 + vec_2) == Vector(4, 5)


def test_subtraction() -> None:
    """
    Vector maths works
    """
    vec_1 = Vector(2, 4)
    vec_2 = Vector(2, 1)
    assert (vec_1 - vec_2) == Vector(0, 3)


def test_absolute_value() -> None:
    """
    Vector absolute value works
    """
    vec = Vector(3, 4)
    assert abs(vec) == 5.0


def test_multiplication() -> None:
    """
    Vector multiplication works
    """
    vec = Vector(3, 4)
    assert vec * 3 == Vector(9, 12)
    assert abs(vec * 3) == 15.0


def test_rotate_90() -> None:
    """
    Vector rotation works
    """
    vec = Vector(3, 4)
    assert vec.rotate_90() == Vector(4, -3)


def test_normalize() -> None:
    """
    Vector normalization works
    """
    vec = Vector(3, 4)
    normalized = vec.normalize()
    assert isclose(normalized.x, 0.6)
    assert isclose(normalized.y, 0.8)


def test_equality() -> None:
    """
    Vector equality works
    """
    vec_1 = Vector(3, 4)
    vec_2 = Vector(3, 4)
    assert vec_1 == vec_2
    assert vec_1 != Vector(0, 0)
    assert vec_1 != 3


def test_truthiness() -> None:
    """
    Vector truthiness works
    """
    vec = Vector(3, 4)
    assert vec
    assert bool(Vector(0, 0)) is False
