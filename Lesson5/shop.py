from constants import (
    FREE_SHIPPING_THRESHOLD,
    HIGH_VALUE_DISCOUNT_RATE,
    HIGH_VALUE_DISCOUNT_THRESHOLD,
    MAX_ITEMS_PER_ORDER,
    MID_VALUE_DISCOUNT_RATE,
    MID_VALUE_DISCOUNT_THRESHOLD,
    OrderStatus,
    PAYMENT_TIMEOUT_SECONDS,
    SHIPPING_COST,
    CustomerType,
    VIP_DISCOUNT_RATE,
)


STATUS_TRANSITIONS = {
    OrderStatus.NEW: OrderStatus.PAID,
    OrderStatus.PAID: OrderStatus.SHIPPED,
    OrderStatus.SHIPPED: OrderStatus.DELIVERED,
}


def calculate_discount(total, customer_type):
    if customer_type == CustomerType.VIP:
        return total * VIP_DISCOUNT_RATE
    if total >= HIGH_VALUE_DISCOUNT_THRESHOLD:
        return total * HIGH_VALUE_DISCOUNT_RATE
    if total >= MID_VALUE_DISCOUNT_THRESHOLD:
        return total * MID_VALUE_DISCOUNT_RATE
    return 0


def shipping_cost(total):
    if total >= FREE_SHIPPING_THRESHOLD:
        return 0
    return SHIPPING_COST


def next_status(status):
    next_order_status = STATUS_TRANSITIONS.get(status)
    if next_order_status is not None:
        return next_order_status
    raise ValueError("Нельзя перейти из статуса " + status)


def can_cancel(order):
    return order["status"] in (OrderStatus.NEW, OrderStatus.PAID)


def is_payment_expired(order, now):
    return (
        (now - order["created_at"]).total_seconds()
        > PAYMENT_TIMEOUT_SECONDS
    )


def validate_items_count(items):
    if len(items) > MAX_ITEMS_PER_ORDER:
        raise ValueError("Слишком много позиций")
