"""Точка входа."""

import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from httpx import AsyncClient

from api.base_router import main_router
from config import settings
from core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Предстартовые настройки."""
    setup_logging()
    logger.info("Запуск %s", settings.app_name)
    logger.info("Параметры запуска - ")
    app.state.gamma_client = AsyncClient(
        base_url=settings.gamma_base_url,
        timeout=settings.gamma_timeout,
        http2=True,
    )
    app.state.clob_client = AsyncClient(
        base_url=settings.clob_base_url,
        timeout=settings.clob_timeout,
        http2=True,
    )
    try:
        yield
    finally:
        app.state.clietn.aclose()
    logger.info("Приложение остановлено.")


def create_app() -> FastAPI:
    """Сборщик приложения."""

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.include_router(
        main_router,
    )

    return app


app = create_app()
