import pytest

from pysquaredle.vector import Vector


class TestVector:
    """
    Vector math tests
    """

    def test_str(self):
        """
        Vector can be converted to a string
        """
        vec = Vector(2, 4)
        assert str(vec) == "(2, 4)"

    def test_repr(self):
        """
        Vector can be converted to a string
        """
        vec = Vector(2, 4)
        assert repr(vec) == "Vector(2, 4)"

    def test_addition(self):
        """
        Vector maths works
        """
        vec_1 = Vector(2, 4)
        vec_2 = Vector(2, 1)
        assert (vec_1 + vec_2) == Vector(4, 5)

    def test_absolute_value(self):
        """
        Vector absolute value works
        """
        vec = Vector(3, 4)
        assert abs(vec) == 5.0

    def test_multiplication(self):
        """
        Vector multiplication works
        """
        vec = Vector(3, 4)
        assert vec * 3 == Vector(9, 12)
        assert abs(vec * 3) == 15.0

    def test_rotate_90(self):
        """
        Vector rotation works
        """
        vec = Vector(3, 4)
        assert vec.rotate_90() == Vector(4, -3)

    def test_normalize(self):
        """
        Vector normalization works
        """
        vec = Vector(3, 4)
        normalized = vec.normalize()
        assert normalized.x == pytest.approx(0.6)
        assert normalized.y == pytest.approx(0.8)
