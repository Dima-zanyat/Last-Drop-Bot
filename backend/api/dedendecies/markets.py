"""Менеджер зависимостей /markets."""

from typing import Annotated
from fastapi import Request, Depends
from services.polymarket.gamma import GammaClient
from services.polymarket.clob import ClobClient


def get_gamma_api(request: Request) -> GammaClient:
    """Извлекает httpx.AsyncClient из state приложения и инициализирует GammaClient."""
    client = request.app.state.gamma_client
    return GammaClient(client)


def get_clob_api(request: Request) -> ClobClient:
    """Извлекает httpx.AsyncClient из state приложения и инициализирует ClobClient."""
    client = request.app.state.clob_client
    return ClobClient(client)


DepGammaApi = Annotated[GammaClient, Depends(get_gamma_api)]
DepClobApi = Annotated[ClobClient, Depends(get_clob_api)]
