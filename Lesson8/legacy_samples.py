"""Legacy classroom examples retained for safe refactoring practice."""


def evaluate(flag):
    """Return a label for a boolean flag."""
    if flag is True:
        return "yes"
    return "no"


def risky_conversion(value):
    """Convert a value to an integer, or return None for invalid input."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def lookup(records, key):
    """Return a record if the key exists, otherwise return None."""
    return records.get(key)


def show_value(value):
    """Print the supplied value."""
    print(value)
