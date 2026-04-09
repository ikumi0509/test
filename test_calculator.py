import pytest
from calculator import add, subtract, multiply, divide


# --- 足し算 ---
def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 0) == 0


# --- 引き算 ---
def test_subtract_basic():
    assert subtract(10, 3) == 7


def test_subtract_negative_result():
    assert subtract(3, 10) == -7


# --- 掛け算 ---
def test_multiply_basic():
    assert multiply(4, 5) == 20


def test_multiply_by_zero():
    assert multiply(100, 0) == 0


# --- 割り算 ---
def test_divide_basic():
    assert divide(10, 2) == 5.0


def test_divide_float_result():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="ゼロで割ることはできません"):
        divide(10, 0)
