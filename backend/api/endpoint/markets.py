"""Роутер для получения данных с Gamma API."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
import httpx

from api.dedendecies.markets import DepGammaApi
from models.gamma import CryptoMarket
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
