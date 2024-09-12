from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import CurrentUser
from app.api.dependencies.projects import check_project_ownership
from app.api.dependencies.services import TaskServiceDep
from app.schemas.response import TodoistResponse
from app.schemas.tasks import TaskData, TaskToUpdate, TaskInResponse

router = APIRouter(
    prefix="/tasks"
)


@router.get(
    "/{task_uid}",
    response_model=TaskInResponse[TaskData],
    name="tasks:create_task",
    dependencies=[Depends(check_project_ownership)]
)
async def get_task(
        task_uid: str,
        task_service: TaskServiceDep,
        current_user: CurrentUser,
) -> TaskInResponse:
    task = await task_service.get_task(current_user, task_uid)

    return TaskInResponse(**task.dict())


@router.delete(
    "/{task_uid}",
    response_model=TodoistResponse,
    name="tasks:delete",
)
async def delete_task(
        task_uid: str,
        task_service: TaskServiceDep,
        current_user: CurrentUser,
) -> TodoistResponse:
    await task_service.delete_task(current_user, task_uid)

    return TodoistResponse(
        success=True
    )


@router.put(
    '/{task_id}',
    response_model=TodoistResponse[TaskData],
    name="tasks:update",
)
async def update_task(
        task_uid: str,
        task_to_update: TaskToUpdate,
        task_service: TaskServiceDep,
        current_user: CurrentUser,
) -> TodoistResponse[TaskData]:
    updated_task = await task_service.update_task(
        current_user, task_uid, task_to_update
    )
    return TodoistResponse[TaskData](
        success=True,
        data=updated_task,
    )
