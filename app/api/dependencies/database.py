from fastapi import Depends, Request
from asyncpg import Pool, Connection
from app.db.repositories.base import BaseRepository
from typing import Type, Annotated


async def _get_connection_from_pool(request: Request):
    pool: Pool = request.app.state.pool

    async with pool.acquire() as connection:
        yield connection


def get_repository(
    repo_type: Type[BaseRepository],
):
    def _get_repo(
        connection: Connection = Depends(_get_connection_from_pool)
    ):
        return repo_type(connection)

    return _get_repo


DbConnectionDep = Annotated[Connection, Depends(_get_connection_from_pool)]