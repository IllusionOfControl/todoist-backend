from fastapi import FastAPI, Depends, Path, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from pydantic import BaseModel
from datetime import datetime, timedelta
import asyncpg
import jwt
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.db.repositories.projects import ProjectsRepository
from app.models.domains.users import UserDomain
from app.models.domains.projects import ProjectDomain
from app.models.schemas.users import UserInSignup, UserInResponse, UserInSignin
from app.models.schemas.projects import ProjectInResponse, ListOfProjectsInResponse, ProjectInCreate, ProjectInUpdate
from app.services.authentication import check_username_is_taken, check_email_is_taken
from app.services.jwt import create_access_token_for_user
from app.api.dependencies.authentication import get_current_user_authorizer
from loguru import logger
from typing import Callable


# TODO: Rewrite main.py
# TODO: Add config system
# TODO: Add logging with loguru
# TODO: Add error handling
# TODO: Move duplicate code to dependencies

app = FastAPI(
    docs_url="/docs",
)


def create_start_app_handler(
    app: FastAPI,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to PostgreSQL")

    app.state.pool = await asyncpg.create_pool(
        "postgresql://postgres:Qw123456@postgres.turnkey.vm/todoist",
        min_size=2,
        max_size=2,
    )

    logger.info("Connection established")

app.add_event_handler(
    "startup",
    create_start_app_handler(app),
)


@app.get('/user/{username}')
async def retrieve_profile_by_username(
    username: str = Path(..., min_length=3),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    return await user_repo.get_user_by_username(username=username)


@app.post('/auth/signup')
async def register_user(
    user_signup: UserInSignup = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    if await check_username_is_taken(users_repo, user_signup.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            # detail=strings.USERNAME_TAKEN,
        )

    if await check_email_is_taken(users_repo, user_signup.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            # detail=strings.EMAIL_TAKEN,
        )
    user = await users_repo.create_user(**user_signup.dict())

    token = create_access_token_for_user(
        user,
        "SECRET"
    )
    return UserInResponse(**user.dict(), token=token)


@app.post('/auth/signin')
async def login_user(
    user_login: UserInSignin = Body(...),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        # detail=strings.INCORRECT_LOGIN_INPUT,
    )

    try:
        user = await user_repo.get_user_by_username(username=user_login.username)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = create_access_token_for_user(
        user,
        "SECRET"
    )
    return UserInResponse(**user.dict(), token=token)


@app.post('/projects')
async def create_project(
    new_project: ProjectInCreate = Body(...),
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer())
):
    project = await project_repo.create_project(title=new_project.title, user=user)

    return ProjectInResponse(**project.dict())


@app.get(
    '/projects',
    response_model=ListOfProjectsInResponse
)
async def get_all_projects(
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer())
) -> ListOfProjectsInResponse:
    projects = await project_repo.get_all_projects(user=user)

    projects_for_response = [
        ProjectInResponse(**project.dict()) for project in projects
    ]

    return ListOfProjectsInResponse(
        projects=projects_for_response,
        count=len(projects_for_response)
    )


@app.get('/project/{project_id}')
async def retrieve_project_by_id(
    project_id: int,
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer())
) -> ProjectInResponse:
    project = await project_repo.get_project(user=user, project_id=int(project_id))

    return ProjectInResponse(**project.dict())


# TODO: rewrite
@app.put('/project/{project_id}')
async def update_project(
    project_id: int,
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer()),
    project_update: ProjectInUpdate = Body(...)
) -> ProjectInResponse:
    project = await project_repo.get_project(user=user, project_id=project_id)
    new_project = await project_repo.update_project(
        project=project,
        **project_update.dict()
    )
    return ProjectInResponse(**new_project.dict())


@app.delete(
    '/project/{project_id}',
    status_code=HTTP_204_NO_CONTENT,
)
async def remove_project(
    project_id: int,
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer())
):
    await project_repo.remove_project(user=user, project_id=project_id)


# TODO: Rewrote endpoint names. example: update_project_by_id
# TODO: Rewrite dependencies to get_projects_by_slug_from_path and check_article_modification_permissions
