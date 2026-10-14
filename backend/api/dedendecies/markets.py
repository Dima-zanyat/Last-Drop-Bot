"""Менеджер зависимостей /markets."""

from typing import Annotated
from fastapi import Request, Depends
from services.polymarket.gamma import GammaClient


def get_gamma_api(request: Request) -> GammaClient:
    """Извлекает httpx.AsyncClient из state приложения и инициализирует GammaClient."""
    client = request.app.state.client
    return GammaClient(client)


DepGammaApi = Annotated[GammaClient, Depends(get_gamma_api)]
