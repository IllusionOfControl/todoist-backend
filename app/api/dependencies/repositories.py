from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database import DatabaseSessionDep
from app.database.repositories.users import UsersRepository


def get_user_repository(
        session: DatabaseSessionDep
) -> UsersRepository:
    return UsersRepository(session)


UsersRepositoryDep = Annotated[UsersRepository, Depends(get_user_repository)]
