"""
main.py
-------
This is the ENTRY POINT of the program - the file you actually run.
It only handles user interaction (input/output). All the real logic
lives in password_checker.py. This split makes the project easier to
test and easier to extend later (e.g. adding a GUI would only mean
writing a new interface file, not touching the logic at all).
"""

from password_checker import check_password_strength


def print_report(result: dict) -> None:
    """Nicely print the password strength report to the console."""
    print("\n----- Password Strength Report -----")
    print(f"Password        : {'*' * result['length']}")
    print(f"Length          : {result['length']}")
    print(f"Uppercase used  : {'Yes' if result['has_upper'] else 'No'}")
    print(f"Lowercase used  : {'Yes' if result['has_lower'] else 'No'}")
    print(f"Numbers used    : {'Yes' if result['has_digit'] else 'No'}")
    print(f"Symbols used    : {'Yes' if result['has_symbol'] else 'No'}")
    print(f"Common password : {'Yes (found in leaked-password list!)' if result['is_common'] else 'No'}")
    print(f"Sequential chars: {'Yes (e.g. 1234, abcd)' if result['has_sequence'] else 'No'}")
    print(f"Repeated chars  : {'Yes (e.g. aaa, 111)' if result['has_repeat'] else 'No'}")
    print(f"Entropy         : {result['entropy_bits']} bits")
    print(f"Score           : {result['score']} / 6")
    print(f"Strength        : {result['strength']}")
    print("-------------------------------------\n")


def main():
    print("=== Password Strength Checker ===")
    print("Type 'q' at any time to quit.\n")

    while True:
        password = input("Enter a password to check: ")

        if password.lower() == "q":
            print("Exiting. Stay secure!")
            break

        if password == "":
            print("Password cannot be empty. Try again.\n")
            continue

        result = check_password_strength(password)
        print_report(result)


if __name__ == "__main__":
    main()
