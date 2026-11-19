import pytest
from shop import calculate_discount


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (1000, 20, 800.0),
        (500, 0, 500.0),
        (1500, 100, 0.0),
        (0, 25, 0.0),
    ],
)
def test_calculate_discount_parametrized(price, discount, expected):
    result = calculate_discount(price, discount)
    assert result == expected