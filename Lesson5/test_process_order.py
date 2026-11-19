import pytest

from orders import DB, OUTBOX, process_order


@pytest.fixture(autouse=True)
def clean():
    DB.clear()
    OUTBOX.clear()


def make_order(**kw):
    order = {
        "id": 1,
        "customer_email": "a@b.ru",
        "items": [{"price": 1000, "qty": 2}],
        "delivery": "courier",
    }
    order.update(kw)
    return order


def test_courier_small_order():
    record = process_order(make_order())
    assert record["total"] == 2000
    assert record["delivery"] == 300
    assert record["final_total"] == 2300
    assert record["bonus"] == 20


def test_big_order_discount_free_delivery():
    record = process_order(make_order(items=[{"price": 6000, "qty": 2}]))
    assert record["total"] == 10800
    assert record["delivery"] == 0
    assert record["bonus"] == 108


def test_coupon_and_vip():
    record = process_order(
        make_order(
            items=[{"price": 1000, "qty": 5}],
            coupon="SALE10",
            is_vip=True,
            delivery="pickup",
        )
    )
    assert record["total"] == 4146.75
    assert record["bonus"] == 82


def test_saves_and_sends_email():
    process_order(make_order())
    assert len(DB) == 1
    assert OUTBOX[0]["to"] == "a@b.ru"
    assert OUTBOX[0]["subject"] == "Заказ 1 принят"


def test_bad_email():
    with pytest.raises(ValueError):
        process_order(make_order(customer_email="abc"))


def test_empty_items():
    with pytest.raises(ValueError):
        process_order(make_order(items=[]))
