"""Роутер для получения данных с Gamma API."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
import httpx

from api.dedendecies.markets import DepGammaApi, DepClobApi
from models.gamma import CryptoMarket
from models.clob import OrderBook
from config import settings

router = APIRouter(tags=["markets"])
logger = logging.getLogger(__name__)


@router.get("/crypto/5m")
async def get_crypto_5m_markets(gamma: DepGammaApi) -> list[CryptoMarket]:
    try:
        return await gamma.get_current_crypto_event(settings.assert_marker)
    except httpx.TimeoutException as exc:
        logger.warning("Истекло время ожидания ответа Gamma")
        raise HTTPException(
            status_code=504,
            detail="Gamma API не ответил вовремя",
        ) from exc
    except httpx.HTTPStatusError as exc:
        logger.exception(
            "Gamma API вернул HTTP %s",
            exc.response.status_code,
        )
        raise HTTPException(
            status_code=502,
            detail="Gamma API вернул ошибку",
        ) from exc
    except httpx.RequestError as exc:
        logger.exception("Ошибка соединения с Gamma API")
        raise HTTPException(
            status_code=502,
            detail="Не удалось подключиться к Gamma API",
        ) from exc
    except ValueError as exc:
        logger.exception("Некорректный ответ Gamma API")
        raise HTTPException(
            status_code=502,
            detail="Gamma API вернул некорректные данные",
        ) from exc


@router.get("/market-order")
async def get_market_order(
    client: DepClobApi,
    token_id: str,
) -> OrderBook:
    try:
        return await client.to_snapshot(token_id=token_id)
    except httpx.TimeoutException as exc:
        logger.exception("Истекло время ожидания от Clob")
        raise HTTPException(status_code=504, detail="Clob не ответи вовремя.") from exc
    except httpx.HTTPStatusError as exc:
        logger.exception("API вернул HTTP - %s", exc.response.status_code)
        raise HTTPException(status_code=502, detail="API вернул ошибку")
    except httpx.RequestError as exc:
        logger.exception("Ошибка соединения с Clob API")
        raise HTTPException(
            status_code=502,
            detail="Не удалось подключиться к Clob API",
        ) from exc
    except ValueError as exc:
        logger.exception("Некорректный ответ Clob API")
        raise HTTPException(
            status_code=502,
            detail="Gamma API вернул некорректные данные",
        ) from exc
    finally:
        await client.close()


@router.get("best-ask-bid")
async def best_ask_bid():
    """"""
