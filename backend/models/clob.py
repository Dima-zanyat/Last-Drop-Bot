"""Модели торговых данных CLOB."""

import logging
from datetime import datetime, timezone
from dataclasses import dataclass
from decimal import Decimal

import orjson

from models.utils.parser import parse_data

logger = logging.getLogger(__name__)


class ClobDataError(Exception):
    """ "Некоректные данные в ответе gamma."""


@dataclass(frozen=True, slots=True)
class OrderBookLevel:
    """Уровень стакана: цена и доступный объем."""

    price: Decimal
    size: Decimal


@dataclass(frozen=True, slots=True)
class OrderBook:
    """Снимок стакана одного исхода."""

    token_id: str
    timestamp: int
    bids: tuple[OrderBookLevel, ...]
    asks: tuple[OrderBookLevel, ...]

    @property
    def best_ask(self) -> OrderBookLevel | None:
        """Лучшая цена для покупки."""
        return self.asks[-1] if self.asks else None

    @property
    def best_bid(self) -> OrderBookLevel | None:
        """Лучашя цена для продажи."""
        return self.bids[-1] if self.bids else None

    @property
    def timestamp_in_time(self):
        return datetime.fromtimestamp(self.timestamp / 1000, tz=timezone.utc)

    @property
    def midpoint(self) -> Decimal | None:
        """Средняя цена между лучшими bid и ask"""
        if self.best_ask is None or self.best_bid is None:
            return None
        return (self.best_bid.price + self.best_ask.price) / Decimal("2")

    def available_size_up_to(self, max_price: Decimal) -> Decimal:
        """Объем стакана по допустимой цене (аргумент и возврат изменены на Decimal)."""
        if not self.asks:
            return Decimal("0")
        return sum(
            (level.size for level in self.asks if level.price <= max_price),
            start=Decimal("0"),
        )


def parse_order_book_level(cap: list[dict[str, str]]) -> tuple[OrderBookLevel, ...]:
    if not cap:
        return ()
    result = tuple(
        [
            OrderBookLevel(
                price=Decimal(example_cap["price"]),
                size=Decimal(example_cap["size"]),
            )
            for example_cap in cap
        ]
    )
    return result


def parse_clob(raw_data, token_id: str) -> OrderBook:

    data = orjson.loads(raw_data)

    timestamp_raw = data.get("timestamp")
    if timestamp_raw is None:
        logger.warning("В ответе отсутсввует timestamp.")
        raise ClobDataError(f"В ответе отсутсввует timestamp.")
    try:
        timestamp = int(timestamp_raw)
    except (ValueError, TypeError) as exc:
        raise ClobDataError(f"Неудалось преобразовать к int - {timestamp_raw}")
    bids = data.get("bids")
    if bids is None:
        raise ClobDataError("Нет значения bids")
    asks = data.get("asks")
    if asks is None:
        raise ClobDataError("Нет значени asks")
    order_book_bids: tuple[OrderBookLevel, ...] = parse_order_book_level(bids)
    order_book_asks: tuple[OrderBookLevel, ...] = parse_order_book_level(asks)

    return OrderBook(
        token_id=token_id,
        timestamp=timestamp,
        bids=order_book_bids,
        asks=order_book_asks,
    )
