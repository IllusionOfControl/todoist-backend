from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from app.api.dependencies.repositories import TasksRepositoryDep
from app.models.tasks import Task
from app.resourses import strings


async def get_task_by_uid_from_path(
        task_uid: int,
        task_repository: TasksRepositoryDep,
) -> Task:
    task = await task_repository.get_by_uid(task_uid)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PROJECT_DOES_NOT_EXIST_ERROR,
        )
    return task

TaskFromPathDep = Annotated[Task, Depends(get_task_by_uid_from_path)]