from sqlalchemy.ext.asyncio import AsyncSession
from typing import Protocol


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
