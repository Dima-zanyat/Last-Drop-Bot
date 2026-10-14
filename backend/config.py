"""Модуль настройки приложения."""


class Settings:
    """Класс настройки приложения."""

    # FastAPI settings
    app_name = "Last drop bot"
    debug = True

    # logger
    log_level = "INFO"

    # db
    db_echo = True

    # Gamma
    gamma_base_url = "https://gamma-api.polymarket.com"
    gamma_timeout = 10
    assert_marker: tuple[str, ...] = ("btc", "eth", "sol", "xrp")


settings = Settings()
