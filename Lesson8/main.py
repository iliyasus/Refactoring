"""Entry point for the Lesson 8 static-analysis demo."""

from accounts import find_account
from pricing import discount


def main():
    """Run the small demo."""
    accounts = {}
    account = find_account(accounts, "admin")
    total = discount(100, 10)
    print(total, account)


if __name__ == "__main__":
    main()
