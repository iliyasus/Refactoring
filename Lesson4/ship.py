def shipping_cost(order):
    if order is None or not order["items"] or not order["total"] > 0:
        return 0

    if order["country"] != "KZ":
        return 5000
    if order["total"] >= 20000:
        return 0
    return 1500

def can_return(order):
    is_eligible_for_return = (
        order["status"] == "delivered"
        and order["days"] <= 14
        and not order["is_used"]
        and (order["total"] > 0 or order["has_gift"])
    )
    return is_eligible_for_return


assert shipping_cost(None) == 0
assert shipping_cost({"items": [], "country": "KZ", "total": 0}) == 0
assert shipping_cost({"items": [1], "country": "KZ", "total": 25000}) == 0
assert shipping_cost({"items": [1], "country": "KZ", "total": 1000}) == 1500
assert shipping_cost({"items": [1], "country": "RU", "total": 1000}) == 5000

o = {"status": "delivered", "days": 3, "is_used": False, "total": 100, "has_gift": False}
assert can_return(o)
assert not can_return({**o, "days": 15})
assert not can_return({**o, "is_used": True})
assert not can_return({**o, "total": 0})
assert can_return({**o, "total": 0, "has_gift": True})
print("Все тесты пройдены")
