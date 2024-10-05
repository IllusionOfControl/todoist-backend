from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database import DatabaseSessionDep
from app.database.repositories.tasks import TasksRepository
from app.database.repositories.projects import ProjectRepository
from app.database.repositories.users import UsersRepository


def get_user_repository(
        session: DatabaseSessionDep
) -> UsersRepository:
    return UsersRepository(session)


UsersRepositoryDep = Annotated[UsersRepository, Depends(get_user_repository)]


def get_projects_repository(
        session: DatabaseSessionDep
) -> ProjectRepository:
    return ProjectRepository(session)


ProjectsRepositoryDep = Annotated[ProjectRepository, Depends(get_projects_repository)]


def get_tasks_repository(
        session: DatabaseSessionDep
) -> TasksRepository:
    return TasksRepository(session)


TasksRepositoryDep = Annotated[TasksRepository, Depends(get_tasks_repository)]
