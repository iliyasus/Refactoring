import pytest

from orders_v2 import (
    STOCK,
    calculate_bonus,
    calculate_total,
    check_order,
    delivery_days,
    process_order,
    report_books,
    report_food,
    report_tech,
)


@pytest.fixture(autouse=True)
def restore_stock():
    original_stock = STOCK.copy()
    yield
    STOCK.clear()
    STOCK.update(original_stock)


def make_user(**overrides):
    user = {
        "type": "regular",
        "years": 1,
        "active": True,
        "age": 30,
        "city": "Almaty",
    }
    user.update(overrides)
    return user


def test_calculate_total_applies_discount_promo_delivery_and_tax():
    items = [("book", 100, 60, "books")]

    assert calculate_total(items, make_user(type="vip"), "SALE10") == 5748.0


def test_calculate_total_floors_discounted_total_at_zero():
    items = [("book", 100, 1, "books")]

    assert calculate_total(items, None, "NY2024") == 420.0


@pytest.mark.parametrize(
    ("report", "category"),
    [
        (report_food, "food"),
        (report_tech, "tech"),
        (report_books, "books"),
    ],
)
def test_category_reports_include_only_matching_items(report, category):
    items = [
        ("apple", 50, 2, "food"),
        ("phone", 400, 1, "tech"),
        ("novel", 300, 3, "books"),
    ]

    assert report(items) == {
        "food": "1. apple x2 = 100\n",
        "tech": "1. phone x1 = 400\n",
        "books": "1. novel x3 = 900\n",
    }[category]


@pytest.mark.parametrize(
    ("user", "address", "expected"),
    [
        (None, "Abay st. 1", "no_user"),
        (make_user(active=False), "Abay st. 1", "inactive"),
        (make_user(), None, "address"),
        (make_user(), "12345", "address"),
        (make_user(age=17), "Abay st. 1", "age"),
        (make_user(), "Abay st. 1", "ok"),
    ],
)
def test_check_order_returns_expected_validation_status(user, address, expected):
    assert check_order(user, address) == expected


def test_calculate_bonus_and_delivery_days():
    vip = make_user(type="vip", years=6)

    assert calculate_bonus(vip, 12000) == 2550
    assert delivery_days(vip, 12000) == 2
    assert delivery_days(make_user(city="Astana"), 8000) == 7


def test_process_order_success_updates_stock_and_returns_summary():
    user = make_user(type="vip", years=6)
    items = [("apple", 50, 2, "food"), ("phone", 4000, 1, "tech")]

    result = process_order(items, user, "SALE10", "Abay st. 1")

    assert result == {
        "status": "ok",
        "total": 4446.6,
        "bonus": 666,
        "days": 2,
        "text": (
            "ORDER\n"
            "FOOD:\n1. apple x2 = 100\n"
            "TECH:\n1. phone x1 = 4000\n"
            "TOTAL: 4446.6\n"
        ),
    }
    assert STOCK["apple"] == 98
    assert STOCK["phone"] == 4


@pytest.mark.parametrize(
    ("items", "reason"),
    [
        ([("unknown", 10, 1, "food")], "unknown unknown"),
        ([("phone", 10, 6, "tech")], "stock phone"),
    ],
)
def test_process_order_rejects_invalid_stock_without_mutating_it(items, reason):
    original_stock = STOCK.copy()

    result = process_order(items, make_user(), None, "Abay st. 1")

    assert result == {"status": "error", "reason": reason}
    assert STOCK == original_stock
