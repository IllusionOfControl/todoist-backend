from fastapi import FastAPI

from app.core.settings.app import AppSettings
from app.db.events import connect_to_psql, close_psql_connection
from loguru import logger
from typing import Callable


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings
) -> Callable:
    async def start_app() -> None:
        await connect_to_psql(app, settings)

    return start_app


def create_stop_app_handler(
        app: FastAPI,
        settings: AppSettings
) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await close_psql_connection(app)

    return stop_app