from typing import Annotated

from fastapi import Depends

from app.api.dependencies.repositories import UserRepositoryDep, TaskRepositoryDep, ProjectsRepositoryDep
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.services.project import ProjectService
from app.services.authentication import AuthenticationService
from app.services.jwt import JWTService
from app.services.task import TaskService

__all__ = ["JWTServiceDep", "AuthenticationServiceDep", "ProjectServiceDep", "TaskServiceDep"]


def get_jwt_service(
        settings: Annotated[AppSettings, Depends(get_app_settings)],
) -> JWTService:
    return JWTService(settings.security.secret_key.get_secret_value())


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


def get_authentication_service(
        user_repository: UserRepositoryDep,
        jwt_service: JWTServiceDep,
) -> AuthenticationService:
    return AuthenticationService(
        user_repository,
        jwt_service
    )


AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]


def get_project_service(
        projects_repository: ProjectsRepositoryDep,
) -> ProjectService:
    return ProjectService(projects_repository)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]


def get_task_service(
        projects_service: ProjectServiceDep,
        task_repository: TaskRepositoryDep,
) -> TaskService:
    return TaskService(projects_service, task_repository)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
