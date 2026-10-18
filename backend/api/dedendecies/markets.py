"""Менеджер зависимостей /markets."""

from typing import Annotated
from fastapi import Request, Depends
from services.polymarket.gamma import GammaClient
from services.polymarket.clob import ClobClient
from services.collector import Collector


def get_gamma_api(request: Request) -> GammaClient:
    """Извлекает httpx.AsyncClient из state приложения и инициализирует GammaClient."""
    client = request.app.state.gamma_client
    return GammaClient(client)


def get_clob_api(request: Request) -> ClobClient:
    """Извлекает httpx.AsyncClient из state приложения и инициализирует ClobClient."""
    client = request.app.state.clob_client
    return ClobClient(client)


def get_colletc_api(
    gamma_client: Annotated[GammaClient, Depends(get_gamma_api)],
    clob_client: Annotated[ClobClient, Depends(get_clob_api)],
) -> Collector:
    """Собирает общую инфу из Gamma и Clob клиентов."""
    return Collector(
        gamma_client=gamma_client,
        clob_client=clob_client,
    )


DepGammaApi = Annotated[GammaClient, Depends(get_gamma_api)]
DepClobApi = Annotated[ClobClient, Depends(get_clob_api)]
DepCollect = Annotated[Collector, Depends(get_colletc_api)]
