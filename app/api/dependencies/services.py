from typing import Annotated

from fastapi import Depends

from app.api.dependencies.repositories import UsersRepositoryDep, TasksRepositoryDep
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.services.authentication import AuthenticationService
from app.services.jwt import JWTService
from app.services.tasks import TasksService


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


def get_tasks_service(
        task_repository: TasksRepositoryDep,
) -> TasksService:
    return TasksService(task_repository)


TaskServiceDep = Annotated[TasksService, Depends(get_tasks_service)]
