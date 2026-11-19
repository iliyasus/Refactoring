"""Small pricing helpers used by the lesson demo."""

import hmac


def discount(price, percent):
    """Return a price reduced by a percentage."""
    if percent < 0:
        raise ValueError("percent must not be negative")
    if percent > 100:
        return 0
    return price - price * percent / 100


def authenticate(candidate, expected_password):
    """Compare credentials without embedding the expected password."""
    return hmac.compare_digest(
        candidate.encode("utf-8"), expected_password.encode("utf-8")
    )
