import pytest
from datetime import datetime, timedelta

from constants import OrderStatus
from shop import (
    calculate_discount,
    shipping_cost,
    next_status,
    can_cancel,
    is_payment_expired,
    validate_items_count,
)


def test_discount_tiers():
    assert calculate_discount(10000, "regular") == 1000
    assert calculate_discount(5000, "regular") == 250
    assert calculate_discount(100, "regular") == 0
    assert calculate_discount(1000, "vip") == 200


def test_shipping_threshold():
    assert shipping_cost(2999) == 300
    assert shipping_cost(3000) == 0


def test_status_chain():
    assert next_status("new") is OrderStatus.PAID
    assert next_status("new") == "paid"
    assert next_status("paid") == "shipped"
    assert next_status("shipped") == "delivered"
    with pytest.raises(ValueError):
        next_status("delivered")


def test_can_cancel():
    assert can_cancel({"status": "new"})
    assert can_cancel({"status": "paid"})
    assert not can_cancel({"status": "shipped"})


def test_payment_expired():
    now = datetime(2026, 1, 1, 12, 0)
    assert is_payment_expired(
        {"created_at": now - timedelta(seconds=1801)}, now
    )
    assert not is_payment_expired(
        {"created_at": now - timedelta(seconds=1800)}, now
    )


def test_items_limit():
    validate_items_count([1] * 50)
    with pytest.raises(ValueError):
        validate_items_count([1] * 51)
