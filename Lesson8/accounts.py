"""Account lookup helpers used by the lesson demo."""


def find_account(accounts, key):
    """Return the account for key, or None when lookup fails."""
    try:
        return accounts[key]
    except KeyError:
        return None


def is_valid(account):
    """Return whether an account value is present."""
    return bool(account)
