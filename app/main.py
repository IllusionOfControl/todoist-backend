from fastapi import FastAPI, Depends, Path, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.db.repositories.projects import ProjectsRepository
from app.models.domains.users import UserDomain
from app.models.schemas.projects import ProjectInResponse, ListOfProjectsInResponse, ProjectInCreate, ProjectInUpdate
from app.api.dependencies.authentication import get_current_user_authorizer
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.config import get_app_settings
from app.api.routes.api import router


# TODO: Rewrite main.py
# TODO: Write tests
# TODO: Add error handling
# TODO: Move duplicate code to dependencies
# TODO: Add strings

settings = get_app_settings()
settings.configure_logging()

app = FastAPI(
    **settings.fastapi_kwargs
)

app.include_router(router)


app.add_event_handler(
    "startup",
    create_start_app_handler(app, settings),
)

app.add_event_handler(
    "shutdown",
    create_stop_app_handler(app, settings),
)


@app.get('/user/{username}')
async def retrieve_profile_by_username(
    username: str = Path(..., min_length=3),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    return await user_repo.get_user_by_username(username=username)

















# TODO: Rewrote endpoint names. example: update_project_by_id
# TODO: Rewrite dependencies to get_projects_by_slug_from_path and check_article_modification_permissions
