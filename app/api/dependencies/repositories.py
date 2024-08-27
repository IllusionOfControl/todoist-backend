from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database import DbConnectionDep
from app.db.repositories.users import UsersRepository


def get_user_repository(
        connection: DbConnectionDep
) -> UsersRepository:
    return UsersRepository(connection)


UsersRepositoryDep = Annotated[UsersRepository, Depends(get_user_repository)]
