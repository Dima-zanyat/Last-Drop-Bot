"""Парсер для овтетов API."""

from typing import Any

import orjson


def parse_data(
    value: Any, field_name: str, exception_cls: type[Exception]
) -> list[Any]:

    if value is None:
        return []
    try:
        loads_value = orjson.loads(value)
    except orjson.JSONDecodeError as exc:
        raise exception_cls(f"Неулоадсь распарсить - {field_name}") from exc

    if not isinstance(loads_value, list):
        raise exception_cls(f"Поле {field_name} не является списком")

    return loads_value
