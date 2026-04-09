from fizzbuzz import fizzbuzz


def test_fizzbuzz_1():
    assert fizzbuzz(1) == ["1"]


def test_fizzbuzz_3_returns_fizz():
    result = fizzbuzz(3)
    assert result[2] == "Fizz"


def test_fizzbuzz_5_returns_buzz():
    result = fizzbuzz(5)
    assert result[4] == "Buzz"


def test_fizzbuzz_15_returns_fizzbuzz():
    result = fizzbuzz(15)
    assert result[14] == "FizzBuzz"


def test_fizzbuzz_15_full():
    expected = [
        "1", "2", "Fizz", "4", "Buzz",
        "Fizz", "7", "8", "Fizz", "Buzz",
        "11", "Fizz", "13", "14", "FizzBuzz",
    ]
    assert fizzbuzz(15) == expected
