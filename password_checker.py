"""
password_checker.py
--------------------
Core logic for checking password strength.
Kept separate from main.py so the "brain" of the program
is independent from the "interface" (CLI). This is called
separation of concerns - a common practice in real projects.
"""

import string
import math
import os

# Path to the common-password wordlist, relative to this file.
WORDLIST_PATH = os.path.join(os.path.dirname(__file__), "wordlist.txt")


def load_common_passwords(path=WORDLIST_PATH):
    """
    Load a set of well-known weak passwords from a text file.
    Using a set (not a list) makes lookups O(1) instead of O(n).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        # If the wordlist is missing, don't crash - just skip that check.
        return set()


def has_sequential_chars(password: str, run_length: int = 3) -> bool:
    """
    Detect simple sequential patterns like '1234', 'abcd', or keyboard
    runs. We check both ascending and descending sequences of length
    `run_length` anywhere in the password.
    """
    lowered = password.lower()
    for i in range(len(lowered) - run_length + 1):
        chunk = lowered[i:i + run_length]
        codes = [ord(c) for c in chunk]

        ascending = all(codes[j] + 1 == codes[j + 1] for j in range(len(codes) - 1))
        descending = all(codes[j] - 1 == codes[j + 1] for j in range(len(codes) - 1))

        if ascending or descending:
            return True
    return False


def has_repeated_chars(password: str, run_length: int = 3) -> bool:
    """Detect the same character repeated `run_length` times in a row, e.g. 'aaa'."""
    for i in range(len(password) - run_length + 1):
        if len(set(password[i:i + run_length])) == 1:
            return True
    return False


def calculate_entropy(password: str) -> float:
    """
    Estimate password entropy in bits: entropy = length * log2(pool_size)

    'pool_size' is how many possible characters could have been used
    (the bigger the pool, the harder to brute-force). This is a simplified
    approximation of real entropy calculations used in security tools.
    """
    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)

    if pool_size == 0 or len(password) == 0:
        return 0.0

    return len(password) * math.log2(pool_size)


def check_password_strength(password: str) -> dict:
    """
    Run all checks on a password and return a detailed result dict,
    including the final Weak / Medium / Strong verdict.
    """
    common_passwords = load_common_passwords()

    length = len(password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    is_common = password.lower() in common_passwords
    has_sequence = has_sequential_chars(password)
    has_repeat = has_repeated_chars(password)
    entropy = calculate_entropy(password)

    # --- Base scoring (same idea as the basic version) ---
    score = 0
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1

    # --- Penalties for weak patterns ---
    if has_sequence:
        score -= 1
    if has_repeat:
        score -= 1

    score = max(score, 0)  # never let score go negative

    # --- Final verdict ---
    if is_common or length < 8 or score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "password": password,
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "is_common": is_common,
        "has_sequence": has_sequence,
        "has_repeat": has_repeat,
        "entropy_bits": round(entropy, 2),
        "score": score,
        "strength": strength,
    }
