"""
test_checker.py
----------------
Basic unit tests for password_checker.py.

These tests don't need any external library - Python's built-in
'assert' statement is enough for simple checks. Run this file
directly to see PASS/FAIL results printed for each test.
"""

import sys
import os

# Add the parent folder to the path so we can import password_checker.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from password_checker import (
    check_password_strength,
    has_sequential_chars,
    has_repeated_chars,
    calculate_entropy,
)


def test_weak_common_password():
    result = check_password_strength("password")
    assert result["strength"] == "Weak", "A well-known common password should be Weak"
    assert result["is_common"] is True


def test_weak_short_password():
    result = check_password_strength("Ab1!")
    assert result["strength"] == "Weak", "Very short passwords should always be Weak"


def test_strong_password():
    result = check_password_strength("Tr0ub4dor&Zebra!")
    assert result["strength"] == "Strong", "A long, varied password should be Strong"


def test_sequential_detection():
    assert has_sequential_chars("abc123") is True
    assert has_sequential_chars("xk9mQ2") is False


def test_repeated_detection():
    assert has_repeated_chars("aaa111") is True
    assert has_repeated_chars("abcdef") is False


def test_entropy_increases_with_variety():
    low = calculate_entropy("aaaaaaaa")       # lowercase only
    high = calculate_entropy("aA1!aA1!")       # 4 character types
    assert high > low, "Entropy should increase when more character types are used"


def run_all_tests():
    tests = [
        test_weak_common_password,
        test_weak_short_password,
        test_strong_password,
        test_sequential_detection,
        test_repeated_detection,
        test_entropy_increases_with_variety,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__} -> {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")


if __name__ == "__main__":
    run_all_tests()
