"""Simple shop example for the linting exercise."""


def avg(numbers):
    """Return the arithmetic mean of numbers."""
    total = 0
    for number in numbers:
        total += number
    return total / len(numbers)


def find_user(users, name):
    """Return the user whose name matches, or None if no user matches."""
    for user in users:
        if user['name'] == name:
            return user
    return None


class Shop:
    """Store items added to a shop."""

    def __init__(self):
        self.items = []

    def add(self, item, price):
        """Add an item unless its price is unspecified."""
        if price is None:
            return
        self.items.append({'item': item, 'price': price})
