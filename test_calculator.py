import pytest
from calculator import add, sub, mul, div

def test_addition():
    assert add(1, 2) == 3

def test_subtraction():
    assert sub(5, 2) == 3

def test_multiplication():
    assert mul(2, 3) == 6

def test_division():
    assert div(6, 2) == 3

def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        div(2, 0)
