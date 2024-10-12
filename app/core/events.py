from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.core.settings.app import AppSettings
from app.database.events import close_psql_connection, connect_to_psql


def create_start_app_handler(app: FastAPI, settings: AppSettings) -> Callable:
    async def start_app() -> None:
        await connect_to_psql(settings)

    return start_app


def create_stop_app_handler(app: FastAPI, settings: AppSettings) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await close_psql_connection(app)

    return stop_app
