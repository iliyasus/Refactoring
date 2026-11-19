"""Order pricing and fulfillment rules.

Each item is a tuple of (name, unit price, quantity, category).
"""

STOCK = {"apple": 100, "phone": 5, "book": 20, "laptop": 2}

VIP_HIGH_VALUE_THRESHOLD = 5000
VIP_HIGH_VALUE_DISCOUNT = 0.15
VIP_STANDARD_DISCOUNT = 0.05
REGULAR_LONG_TERM_YEARS = 3
REGULAR_LONG_TERM_DISCOUNT = 0.07
REGULAR_HIGH_VALUE_THRESHOLD = 10000
REGULAR_HIGH_VALUE_DISCOUNT = 0.03
PROMO_DISCOUNTS = {"SALE10": 0.1, "SALE20": 0.2}
PROMO_FIXED_DISCOUNTS = {"NY2024": 500}
LOW_ORDER_DELIVERY_THRESHOLD = 3000
HIGH_ORDER_DELIVERY_THRESHOLD = 7000
LOW_ORDER_DELIVERY_COST = 350
HIGH_ORDER_DELIVERY_COST = 200
TAX_RATE = 0.2
CURRENCY_DECIMAL_PLACES = 2
MINIMUM_ADDRESS_LENGTH = 5
MINIMUM_CUSTOMER_AGE = 18
BONUS_RATES = {"vip": 0.1, "regular": 0.05}
DEFAULT_BONUS_RATE = 0.01
HIGH_BONUS_THRESHOLD = 10000
MEDIUM_BONUS_THRESHOLD = 5000
HIGH_BONUS_AMOUNT = 500
MEDIUM_BONUS_AMOUNT = 200
LONG_TERM_CUSTOMER_YEARS = 5
LONG_TERM_BONUS_MULTIPLIER = 1.5
STANDARD_DELIVERY_DAYS = 5
VIP_DELIVERY_DAYS = 2
HIGH_VALUE_DELIVERY_DAYS = 3
NON_ALMATY_DELIVERY_DAYS = 4


def _sum_item_prices(items):
    return sum(price * quantity for _, price, quantity, _ in items)


def _apply_customer_discount(subtotal, user):
    if user is None or not user["active"]:
        return subtotal
    if user["type"] == "vip":
        discount_rate = (
            VIP_HIGH_VALUE_DISCOUNT
            if subtotal > VIP_HIGH_VALUE_THRESHOLD
            else VIP_STANDARD_DISCOUNT
        )
    elif user["type"] == "regular" and user["years"] > REGULAR_LONG_TERM_YEARS:
        discount_rate = REGULAR_LONG_TERM_DISCOUNT
    elif user["type"] == "regular" and subtotal > REGULAR_HIGH_VALUE_THRESHOLD:
        discount_rate = REGULAR_HIGH_VALUE_DISCOUNT
    else:
        return subtotal
    return subtotal * (1 - discount_rate)


def _apply_promotion(subtotal, promo):
    if promo in PROMO_DISCOUNTS:
        return subtotal * (1 - PROMO_DISCOUNTS[promo])
    if promo in PROMO_FIXED_DISCOUNTS:
        return subtotal - PROMO_FIXED_DISCOUNTS[promo]
    return subtotal


def _delivery_cost(subtotal):
    if subtotal < LOW_ORDER_DELIVERY_THRESHOLD:
        return LOW_ORDER_DELIVERY_COST
    if subtotal < HIGH_ORDER_DELIVERY_THRESHOLD:
        return HIGH_ORDER_DELIVERY_COST
    return 0


def calculate_total(items, user, promo):
    subtotal = _sum_item_prices(items)
    subtotal = _apply_customer_discount(subtotal, user)
    subtotal = _apply_promotion(subtotal, promo)
    subtotal = max(subtotal, 0)
    subtotal += _delivery_cost(subtotal)
    subtotal *= 1 + TAX_RATE
    return round(subtotal, CURRENCY_DECIMAL_PLACES)


def _format_category_report(items, category):
    matching_items = (
        (name, price, quantity)
        for name, price, quantity, item_category in items
        if item_category == category
    )
    return "".join(
        f"{number}. {name} x{quantity} = {price * quantity}\n"
        for number, (name, price, quantity) in enumerate(matching_items, start=1)
    )


def report_food(items):
    return _format_category_report(items, "food")


def report_tech(items):
    return _format_category_report(items, "tech")


def report_books(items):
    return _format_category_report(items, "books")


def check_order(user, address):
    if user is None:
        return "no_user"
    if not user["active"]:
        return "inactive"
    if address is None or len(address) <= MINIMUM_ADDRESS_LENGTH:
        return "address"
    if user["age"] < MINIMUM_CUSTOMER_AGE:
        return "age"
    return "ok"


def calculate_bonus(user, total):
    order_total = total
    if user["type"] == "vip":
        bonus = order_total * BONUS_RATES["vip"]
    elif user["type"] == "regular":
        bonus = order_total * BONUS_RATES["regular"]
    else:
        bonus = order_total * DEFAULT_BONUS_RATE
    if order_total > HIGH_BONUS_THRESHOLD:
        bonus += HIGH_BONUS_AMOUNT
    elif order_total > MEDIUM_BONUS_THRESHOLD:
        bonus += MEDIUM_BONUS_AMOUNT
    if user["years"] > LONG_TERM_CUSTOMER_YEARS:
        bonus = bonus * LONG_TERM_BONUS_MULTIPLIER
    return int(bonus)


def delivery_days(user, total):
    order_total = total
    days = STANDARD_DELIVERY_DAYS
    if user["type"] == "vip":
        days = VIP_DELIVERY_DAYS
    else:
        if order_total > HIGH_ORDER_DELIVERY_THRESHOLD:
            days = HIGH_VALUE_DELIVERY_DAYS
    if user["city"] != "Almaty":
        days = days + NON_ALMATY_DELIVERY_DAYS
    return days


def _validate_stock(items):
    for name, _, quantity, _ in items:
        if name not in STOCK:
            return "unknown " + name
        if STOCK[name] < quantity:
            return "stock " + name
    return None


def _deduct_stock(items):
    for name, _, quantity, _ in items:
        STOCK[name] -= quantity


def _format_order_report(items, total):
    report_lines = ["ORDER\n"]
    for heading, category in (
        ("FOOD", "food"),
        ("TECH", "tech"),
        ("BOOKS", "books"),
    ):
        category_report = _format_category_report(items, category)
        if category_report:
            report_lines.append(f"{heading}:\n{category_report}")
    report_lines.append(f"TOTAL: {total}\n")
    return "".join(report_lines)


def process_order(items, user, promo, address):
    validation_status = check_order(user, address)
    if validation_status != "ok":
        return {"status": "error", "reason": validation_status}
    stock_error = _validate_stock(items)
    if stock_error is not None:
        return {"status": "error", "reason": stock_error}

    total = calculate_total(items, user, promo)
    _deduct_stock(items)
    text = _format_order_report(items, total)
    return {
        "status": "ok",
        "total": total,
        "bonus": calculate_bonus(user, total),
        "days": delivery_days(user, total),
        "text": text,
    }


if __name__ == "__main__":
    vip = {"type": "vip", "years": 6, "active": True, "age": 30, "city": "Almaty"}
    order = [("apple", 50, 10, "food"), ("phone", 4000, 1, "tech")]
    print(process_order(order, vip, "SALE10", "Abay st. 1"))
