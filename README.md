# Password Strength Checker

A Python command-line tool that analyzes a password and classifies it as **Weak**, **Medium**, or **Strong** — based on length, character variety, common-password matching, pattern detection, and entropy.

Built as Project 1 for the Cyber Security Internship at **Decode Labs**.

## Project Structure

```
password-strength-checker/
├── main.py                 # CLI entry point (user interaction)
├── password_checker.py     # Core logic (all the actual checks)
├── wordlist.txt            # 1000+ known common/leaked passwords
├── README.md
└── tests/
    └── test_checker.py     # Unit tests for the core logic
```

## Features

- **Length check** — flags short passwords
- **Character variety** — checks for uppercase, lowercase, numbers, and symbols
- **Common password detection** — checks against a list of 1000+ known weak/leaked passwords
- **Pattern detection** — flags sequential runs (`1234`, `abcd`) and repeated characters (`aaa`, `111`)
- **Entropy calculation** — estimates how unpredictable a password is, in bits
- **Score-based verdict** — combines all checks into a final Weak / Medium / Strong rating

## How the Scoring Works

| Criteria | Points |
|---|---|
| Length >= 12 | +2 |
| Length >= 8 | +1 |
| Uppercase letter present | +1 |
| Lowercase letter present | +1 |
| Number present | +1 |
| Symbol present | +1 |
| Sequential pattern found | -1 |
| Repeated characters found | -1 |

Any password found in the common-password list, or shorter than 8 characters, is automatically marked **Weak** regardless of score.

- **Weak**: common password, length < 8, or score <= 2
- **Medium**: score 3-4
- **Strong**: score 5-6

## Usage

```bash
python3 main.py
```

Enter any password when prompted. Type `q` to quit.

### Example

```
=== Password Strength Checker ===
Enter a password to check: P@ssw0rd123!

----- Password Strength Report -----
Password        : ************
Length          : 12
Uppercase used  : Yes
Lowercase used  : Yes
Numbers used    : Yes
Symbols used    : Yes
Common password : No
Sequential chars: No
Repeated chars  : No
Entropy         : 78.66 bits
Score           : 5 / 6
Strength        : Strong
-------------------------------------
```

## Running the Tests

```bash
cd tests
python3 test_checker.py
```

All 6 tests should print `PASS`.

## Skills Demonstrated

- String handling and conditional logic in Python
- Security fundamentals: password entropy, common-password lists, pattern-based weaknesses
- Modular code design (separating logic from interface)
- Writing and running unit tests

## Author

Nitin Yadav — Cyber Security Intern at Decode Labs
