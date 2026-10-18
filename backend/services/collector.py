import logging
from decimal import Decimal

from services.polymarket.gamma import GammaClient
from services.polymarket.clob import ClobClient
from models.gamma import CryptoMarket
from models.clob import OrderBook
from models.collect import Collect, Outcome, Part
from config import settings

logger = logging.getLogger(__name__)


class Collector:

    def __init__(self, gamma_client: GammaClient, clob_client: ClobClient) -> None:
        self._gamma_client = gamma_client
        self._clob_client = clob_client

    async def get_final_result(self) -> list[Collect]:
        """Сборка финального отвта."""
        assert_marker: tuple[str, ...] = settings.assert_marker
        markets: list[CryptoMarket] = await self._gamma_client.get_current_crypto_event(
            assert_marker
        )
        collects: list[Collect] = []
        for market in markets:
            if len(market.outcomes) > 2:
                logger.info("Исходов в ответе - %s", len(market.outcomes))
            outcomes: list = []
            for outcome in market.outcomes:
                order_book: OrderBook = await self._clob_client.to_snapshot(outcome.id)

                if order_book.best_ask is not None:
                    best_part_ask = Part(
                        price=order_book.best_ask.price,
                        size=order_book.best_ask.size,
                    )
                else:
                    best_part_ask = Part(
                        price=Decimal("0"),
                        size=Decimal("0"),
                    )
                if order_book.best_bid is not None:
                    best_part_bid = Part(
                        price=order_book.best_bid.price,
                        size=order_book.best_bid.size,
                    )
                else:
                    best_part_bid = Part(
                        price=Decimal("0"),
                        size=Decimal("0"),
                    )
                outcome = Outcome(
                    label=outcome.label, best_bid=best_part_bid, best_ask=best_part_ask
                )
                outcomes.append(outcome)
            collect = Collect(slug=market.slug, outcomes=tuple(outcomes))
            collects.append(collect)
        return collects
