from app.models.domains.tasks import TaskDomain
from app.models.domains.users import UserDomain
from app.models.domains.projects import ProjectDomain
from app.db.repositories.tasks import TaskRepository
from app.db.repositories.projects import ProjectsRepository
from app.db.errors import EntityDoesNotExist
from app.api.dependencies.database import get_repository
from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.projects import get_project_by_id_from_path
from app.resourses import strings
from fastapi import Depends, HTTPException
from starlette import status


async def get_task_by_id_from_path(
    task_id: int,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
) -> TaskDomain:
    try:
        return await task_repo.get_task_by_id(task_id=task_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PROJECT_DOES_NOT_EXIST_ERROR,
        )
