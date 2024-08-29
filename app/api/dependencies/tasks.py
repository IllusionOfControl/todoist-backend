from app.models.tasks import TaskDomain
from app.database.repositories.tasks import TaskRepository
from app.database.errors import EntityDoesNotExist
from app.api.dependencies.database import get_repository
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
