"""Модуль для создания Gamma клиента."""

import asyncio
from datetime import datetime
import logging
import time
from typing import Any

import httpx

from config import settings
from models.gamma import CryptoMarket, parse_gamma, GammaDataError

logger = logging.getLogger(__name__)


class GammaClient:
    """Клиент Gamma API для поиска рынков."""

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:

        self._client: httpx.AsyncClient = client or httpx.AsyncClient(
            base_url=settings.gamma_base_url,
            timeout=settings.gamma_timeout,
        )

    async def _get_market_by_slug(self, slug: str) -> dict[str, Any] | None:
        """Найти рынок по slug."""
        response = await self._client.get(url="/markets", params={"slug": slug})
        response.raise_for_status()
        markets = response.json()
        if not isinstance(markets, list):
            raise ValueError("Gamma вернул не список рынков.")
        for market in markets:
            if not isinstance(market, dict):
                raise ValueError("Gamma вернул некоректный рынок")
            if market.get("slug") == slug:
                return market
        return None

    async def get_current_crypto_event(
        self, assets: tuple[str, ...]
    ) -> list[CryptoMarket]:

        timestamp = int(time.time())
        window_start = timestamp - timestamp % 300
        slugs = [f"{asset}-updown-5m-{window_start}" for asset in assets]
        markets = await asyncio.gather(
            *(self._get_market_by_slug(slug) for slug in slugs)
        )
        result: list[CryptoMarket] = []
        for slug, market in zip(assets, markets):
            if market is None:
                logger.info("Рынок '%s' не найден", slug)
                continue
            if not self._is_current(market=market):
                logger.exception(f"рынок {slug} недоступен для торговли.")
            try:
                result.append(parse_gamma(market=market))
            except GammaDataError:
                logger.exception(f"Неудалось разобрать рынок - {slug}")

        logger.info(
            "Найдено доступных 5-минутных рынков %s в окне - (%s - %s)",
            len(result),
            datetime.fromtimestamp(window_start).time(),
            datetime.fromtimestamp(window_start + 300).time(),
        )

        return result

    @staticmethod
    def _is_current(market: dict[str, Any]):
        return (
            market.get("active") is True
            and market.get("enableOrderBook") is True
            and market.get("acceptingOrders") is True
        )
