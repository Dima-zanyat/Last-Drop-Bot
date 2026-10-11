"""Точка входа."""

from contextlib import asynccontextmanager
from fastapi import FastAPI


from config import settings
from core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Предстартовые настройки."""
    setup_logging()
    logger.info("Запуск %s", settings.app_name)
    logger.info("Параметры запуска - ")
    yield
    logger.info("Приложение остановлено.")


def create_app() -> FastAPI:
    """Сборщик приложения."""

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    return app


app = create_app()
