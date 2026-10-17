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

    # Gamma API
    gamma_base_url = "https://gamma-api.polymarket.com"
    gamma_timeout = 10
    assert_marker: tuple[str, ...] = ("btc", "eth", "sol", "xrp")

    # CLOB API
    clob_base_url = "https://clob.polymarket.com"
    clob_timeout = 5.0

    # Стратегия наблюдения
    entry_price_min = 0.94
    entry_price_max = 0.96
    min_available_size = 10.0


settings = Settings()
