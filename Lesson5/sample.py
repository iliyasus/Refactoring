DB = []
OUTBOX = []


def validate_order(order):
    if order is None:
        raise ValueError("Заказ не передан")
    if not order.get("customer_email") or "@" not in order["customer_email"]:
        raise ValueError("Некорректный email")
    if not order.get("items"):
        raise ValueError("Пустой заказ")
    for item in order["items"]:
        if item["qty"] <= 0:
            raise ValueError("Некорректное количество")
        if item["price"] < 0:
            raise ValueError("Некорректная цена")


def calculate_total(order):
    total = 0
    for item in order["items"]:
        total += item["price"] * item["qty"]

    if total >= 10000:
        total = total * 0.9
    elif total >= 5000:
        total = total * 0.95
    if order.get("coupon") == "SALE10":
        total = total - total * 0.1
    if order.get("is_vip"):
        total = total * 0.97
    return round(total, 2)


def calculate_delivery_totals(order, total):
    if order.get("delivery") == "courier":
        if total >= 3000:
            delivery = 0
        else:
            delivery = 300
    else:
        delivery = 0
    return delivery, total + delivery


def calculate_bonus(order, total):
    bonus = int(total // 100)
    if order.get("is_vip"):
        bonus = bonus * 2
    return bonus


def save_order(order, total, delivery, final_total, bonus):
    record = {
        "id": order["id"],
        "email": order["customer_email"],
        "total": total,
        "delivery": delivery,
        "final_total": final_total,
        "bonus": bonus,
    }
    DB.append(record)
    return record


def notify_customer(order, final_total):
    OUTBOX.append(
        {
            "to": order["customer_email"],
            "subject": "Заказ " + str(order["id"]) + " принят",
            "body": "Сумма к оплате: " + str(final_total) + " руб.",
        }
    )
    print("Заказ " + str(order["id"]) + " обработан, сумма: " + str(final_total))


def process_order(order):
    validate_order(order)

    total = calculate_total(order)
    delivery, final_total = calculate_delivery_totals(order, total)
    bonus = calculate_bonus(order, total)
    record = save_order(order, total, delivery, final_total, bonus)
    notify_customer(order, final_total)
    return record