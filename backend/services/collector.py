import logging

from services.polymarket.gamma import GammaClient
from services.polymarket.clob import ClobClient
from models.gamma import CryptoMarket
from models.clob import OrderBook
from config import settings

logger = logging.getLogger(__name__)


class Collector:

    def __init__(self, gamma_client: GammaClient, clob_client: ClobClient) -> None:
        self._gamma_client = gamma_client
        self._clob_client = clob_client

    async def get_final_result(self) -> None:
        """Сборка финального отвта."""
        assert_marker: tuple[str, ...] = settings.assert_marker
        markets: list[CryptoMarket] = await self._gamma_client.get_current_crypto_event(
            assert_marker
        )
        for market in markets:
            if len(market.outcomes) > 2:
                logger.info("Исходов в ответе - %s", len(market.outcomes))
            for outcome in market.outcomes:
                orrder_book = await self._clob_client.to_snapshot(outcome.id)
