from __future__ import annotations

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: one way of discounting an order total.

    Order only calls apply() and never checks which strategy it has, so a new
    discount is a new class here and Order does not change (Open/Closed).
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after the discount."""
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged (the default for every Order)."""

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        percentage = float(percentage)
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = percentage

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)

    def __str__(self) -> str:
        return f"{self.__percentage:g}% off"


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) takes $20 off a total of $200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        threshold = float(threshold)
        amount = float(amount)
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        if amount > threshold:
            raise ValueError("Discount amount cannot be more than the threshold.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total

    def __str__(self) -> str:
        return f"${self.__amount:.2f} off orders of ${self.__threshold:.2f} or more"


class StudentDiscount(DiscountStrategy):
    """Section 2.4: a 5% student discount, added without changing Order."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)

    def __str__(self) -> str:
        return "Student discount (5% off)"
