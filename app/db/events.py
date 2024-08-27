import asyncpg
from fastapi import FastAPI
from app.core.settings.app import AppSettings
from loguru import logger


async def connect_to_psql(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    app.state.pool = await asyncpg.create_pool(
        str(settings.postgresql.url),
        min_size=settings.postgresql.min_connection_count,
        max_size=settings.postgresql.max_connection_count,
    )

    logger.info("Connection established")


async def close_psql_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
