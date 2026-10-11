"""Модуль настройки приложения."""

from typing import Literal


class Settings:
    """Класс настройки приложения."""

    # FastAPI settings
    app_name = "Last drop bot"
    debug = True

    # logger
    log_level = "INFO"

    # db
    db_echo = True


settings = Settings()
