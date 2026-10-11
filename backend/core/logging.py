"""Настройка логирования."""

import sys
import logging
from logging.config import dictConfig

from config import settings


def setup_logging():
    dictConfig(
        {
            "version": "0.1.0",
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%m:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": sys.stdout,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": settings.log_level,
            },
            "loggers": {
                "uvicorn.access": {"level": settings.log_level},
                "sqlalchemy.engine": {
                    "level": "INFO" if settings.db_echo else "WARNING",
                },
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
