"""Модуль для clob клиента."""

import logging
import httpx

from config import settings
from models.clob import OrderBook, parse_clob

logger = logging.getLogger(__name__)


class ClobClient:
    """Клиент тольок для чтения."""

    def __init__(self, client: httpx.AsyncClient | None = None):
        self._client = client or httpx.AsyncClient(
            base_url=settings.clob_base_url,
            timeout=settings.clob_timeout,
            http2=True,
        )
        self._is_owned_client = client is None

    async def _get_order_book(self, token_id: str) -> bytes:
        """Запрос на получение данных стакана."""
        try:
            resp = await self._client.get("/book", params={"token_id": token_id})
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.warning("Api вернул ошибку", exc_info=exc)
            raise
        return resp.content

    async def to_snapshot(self, token_id: str) -> OrderBook:
        """Снимок рынка."""

        raw_data: bytes = await self._get_order_book(token_id=token_id)
        snapshot = parse_clob(raw_data=raw_data, token_id=token_id)
        return snapshot

    async def close(self):
        if self._is_owned_client:
            await self._client.aclose()
