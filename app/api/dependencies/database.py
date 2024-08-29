from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import database


async def get_database_session() -> AsyncSession:
    async with database.session() as session:
        yield session


DatabaseSessionDep = Annotated[AsyncSession, Depends(get_database_session)]
