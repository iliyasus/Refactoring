"""Regression tests for the Lesson 8 helpers."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import MagicMock

from accounts import find_account, is_valid
from legacy_samples import lookup, risky_conversion, show_value
from pricing import authenticate, discount


class Lesson8Tests(unittest.TestCase):
    """Check corrected error handling and input validation."""

    def test_find_account_returns_none_for_missing_key(self):
        """A missing account is reported as None."""
        self.assertIsNone(find_account({}, "missing"))

    def test_find_account_does_not_hide_unexpected_errors(self):
        """Unexpected mapping errors propagate to the caller."""
        accounts = MagicMock()
        accounts.__getitem__.side_effect = RuntimeError("storage unavailable")
        with self.assertRaises(RuntimeError):
            find_account(accounts, "user")

    def test_is_valid_returns_boolean(self):
        """The account validity helper returns a bool."""
        self.assertIs(is_valid({"id": 1}), True)
        self.assertIs(is_valid(None), False)

    def test_risky_conversion_handles_invalid_values(self):
        """Invalid integer values return None without hiding other errors."""
        self.assertEqual(risky_conversion("12"), 12)
        self.assertIsNone(risky_conversion("not an integer"))
        self.assertIsNone(risky_conversion(None))

    def test_lookup_returns_none_for_missing_key(self):
        """A missing record is reported as None."""
        self.assertIsNone(lookup({}, "missing"))
        self.assertEqual(lookup({"id": 1}, "id"), 1)

    def test_show_value_prints_its_argument(self):
        """The display helper uses its supplied value."""
        output = StringIO()
        with redirect_stdout(output):
            show_value("ready")
        self.assertEqual(output.getvalue(), "ready\n")

    def test_discount_rejects_negative_percent(self):
        """A negative discount percentage is rejected."""
        with self.assertRaises(ValueError):
            discount(100, -1)
        self.assertEqual(discount(100, 10), 90)
        self.assertEqual(discount(100, 101), 0)

    def test_authenticate_uses_the_supplied_password(self):
        """Credential comparison uses a caller-supplied expected value."""
        self.assertTrue(authenticate("sample", "sample"))
        self.assertFalse(authenticate("wrong", "sample"))


if __name__ == "__main__":
    unittest.main()
