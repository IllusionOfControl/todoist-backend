from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.core.settings.app import DatabaseSettings

__all__ = ("Base", "Database", "database")

Base = declarative_base()


class Database:
    def __init__(self) -> None:
        self._is_initialized = False
        self._engine: AsyncEngine | None = None
        self._session = None

    def connect(self, settings: DatabaseSettings) -> None:
        self._engine = create_async_engine(str(settings.url.unicode_string()), echo=True, pool_size=10, pool_recycle=3600)
        self._session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    async def close(self) -> None:
        await self._engine.dispose()

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def check_connection(self) -> None:
        from sqlalchemy import select

        session: AsyncSession = self._session()
        await session.execute(select(1))

    @asynccontextmanager
    async def context_session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session()
        try:
            yield session
            await session.commit()
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()


database = Database()
