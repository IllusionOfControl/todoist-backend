from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_user_authorizer
from app.db.errors import EntityDoesNotExist
from app.db.repositories.projects import ProjectsRepository
from app.models.domains.users import UserDomain
from app.models.domains.projects import ProjectDomain
from app.resourses import strings
from fastapi import Depends, HTTPException
from starlette import status


async def get_project_by_id_from_path(
    project_id: int,
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
) -> ProjectDomain:
    try:
        return await project_repo.get_project_by_id(project_id=project_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PROJECT_DOES_NOT_EXIST_ERROR,
        )


def check_project_ownership(
    current_project: ProjectDomain = Depends(get_project_by_id_from_path),
    user: UserDomain = Depends(get_current_user_authorizer())
) -> None:
    if not current_project.owner_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.USER_IS_NOT_OWNER_OF_PROJECT,
        )
