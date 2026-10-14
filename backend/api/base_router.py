"""Базовый роутер для всез подключений."""

from fastapi import APIRouter

from api.endpoint import markets

main_router = APIRouter()

main_router.include_router(markets.router)
