"""Модель для проверки ответа gamma и clob"""

from dataclasses import dataclass

from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Part:
    price: Decimal
    size: Decimal


@dataclass(slots=True, frozen=True)
class Outcome:

    label: str
    best_bid: Part
    best_ask: Part


@dataclass(slots=True, frozen=True)
class Collect:

    slug: str
    outcomes: tuple[Outcome, ...]
