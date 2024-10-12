from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database import DatabaseSessionDep
from app.database.repositories.task import TaskRepository
from app.database.repositories.project import ProjectRepository
from app.database.repositories.user import UserRepository


def get_user_repository(
        session: DatabaseSessionDep
) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_project_repository(
        session: DatabaseSessionDep
) -> ProjectRepository:
    return ProjectRepository(session)


ProjectsRepositoryDep = Annotated[ProjectRepository, Depends(get_project_repository)]


def get_task_repository(
        session: DatabaseSessionDep
) -> TaskRepository:
    return TaskRepository(session)


TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
