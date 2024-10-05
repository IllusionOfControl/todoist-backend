from typing import Annotated

from fastapi import Depends

from app.api.dependencies.repositories import UsersRepositoryDep, TasksRepositoryDep, ProjectsRepositoryDep
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.services.projects import ProjectsService
from app.services.authentication import AuthenticationService
from app.services.jwt import JWTService
from app.services.tasks import TaskService

__all__ = ["JWTServiceDep", "AuthenticationServiceDep", "ProjectsServiceDep", "TasksServiceDep"]


def get_jwt_service(
        settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> JWTService:
    return JWTService(settings.security.secret_key.get_secret_value())


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


def get_authentication_service(
        user_repository: UsersRepositoryDep,
        jwt_service: JWTServiceDep,
) -> AuthenticationService:
    return AuthenticationService(
        user_repository,
        jwt_service
    )


AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]


def get_project_service(
        projects_repository: ProjectsRepositoryDep,
) -> ProjectsService:
    return ProjectsService(projects_repository)


ProjectsServiceDep = Annotated[ProjectsService, Depends(get_project_service)]


def get_task_service(
        task_repository: TasksRepositoryDep,
) -> TaskService:
    return TaskService(task_repository)


TasksServiceDep = Annotated[TaskService, Depends(get_task_service)]
