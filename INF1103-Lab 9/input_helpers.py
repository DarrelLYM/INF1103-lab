from __future__ import annotations


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number greater than zero.

    float() raises ValueError for text like "abc" (exception handling),
    and the if statement rejects zero or negative numbers (validation).
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number of 0 or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number greater than zero."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 3")
