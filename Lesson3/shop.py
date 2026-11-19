import requests


def calculate_discount(price, discount_percent):
    if not isinstance(price, (int, float)) or not isinstance(discount_percent, (int, float)):
        raise TypeError("Значения должны быть числами")

    if price < 0 or discount_percent < 0:
        raise ValueError("Значения не могут быть отрицательными")

    if discount_percent > 100:
        raise ValueError("Скидка не может быть больше 100%")

    return price - (price * (discount_percent / 100))


def fetch_exchange_rate(currency):
    """Получает курс валюты относительно RUB."""
    response = requests.get(
        f"https://api.exchangerate.host/latest?base=RUB&symbols={currency}"
    )
    response.raise_for_status()
    return response.json()["rates"][currency]


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item_name, price):
        self.items.append({"name": item_name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def get_total(self):
        return self.total()

    @staticmethod
    def fetch_exchange_rate(currency):
        """Делает реальный сетевой запрос (в тестах его нужно избегать!)."""
        return fetch_exchange_rate(currency)

    def get_cart_total_in_currency(self, currency):
        """Возвращает сумму корзины в другой валюте."""
        rate = self.fetch_exchange_rate(currency)
        return self.total() * rate
