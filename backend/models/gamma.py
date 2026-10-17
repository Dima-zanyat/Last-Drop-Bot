"""Модели для данных Gamma API."""

import json

from dataclasses import dataclass
from typing import Any

from models.utils.parser import parse_data


class GammaDataError(ValueError):
    """Некоректные данные в ответе Gamma."""


@dataclass(frozen=True, slots=True)
class MarketOutcome:
    """Торгуемый исход рынка."""

    label: str
    id: str
    price: float | None


@dataclass(frozen=True, slots=True)
class CryptoMarket:
    """5 минтуный крипторынок."""

    id: str
    slug: str
    question: str
    window_start: int
    outcomes: tuple[MarketOutcome, ...]

    @property
    def up_outcome(self) -> MarketOutcome:
        """Исход UP."""
        return self._get_outcome("Up")

    @property
    def down_outcome(self) -> MarketOutcome:
        """Исход DOWN."""
        return self._get_outcome("Down")

    def _get_outcome(self, label: str) -> MarketOutcome:
        for outcome in self.outcomes:
            if outcome.label == label:
                return outcome
        raise GammaDataError(f"У рынка {self.slug} отсутствует исход - {label}")


def parse_gamma(market: dict[str, Any]):
    """Парсинг в датакласс."""
    id = market.get("id")
    if id is None:
        raise GammaDataError("Поле id отсутствует")
    slug = market.get("slug", "")
    if slug == "":
        raise GammaDataError("Gamma вернул пустое значение slug.")
    question = market.get("question", "")
    if question == "":
        raise GammaDataError(f"question - '{question}' - Описание рынка некоректно.")
    window_start = parse_window_start(slug)

    labels: list[str] = parse_data(market.get("outcomes"), "outcomes", GammaDataError)
    ids: list[str] = parse_data(
        market.get("clobTokenIds"), "clobTokenIds", GammaDataError
    )
    prices_string: list[str] = parse_data(
        market.get("outcomePrices"), "outcomePrices", GammaDataError
    )

    decimal_prices: list[float] = []
    for price in prices_string:
        try:
            decimal_price: float = float(price)
            decimal_prices.append(decimal_price)
        except ValueError:
            raise GammaDataError(f"Неудалось преобразовать в число - {price}")

    market_outcome = tuple(
        MarketOutcome(
            label=label,
            id=id,
            price=price,
        )
        for label, id, price in zip(labels, ids, decimal_prices)
    )

    return CryptoMarket(
        id=id,
        slug=slug,
        question=question,
        window_start=window_start,
        outcomes=market_outcome,
    )


def parse_window_start(slug: str) -> int:
    try:
        return int(slug.split("-")[-1])
    except ValueError as exc:
        raise GammaDataError(
            f"Неудалось извлечь начало окна из slug -{slug}",
        ) from exc
