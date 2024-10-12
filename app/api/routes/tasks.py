from fastapi import APIRouter
from starlette import status

from app.api.dependencies.authentication import CurrentUserDep
from app.api.dependencies.services import ProjectServiceDep, TaskServiceDep
from app.schemas.response import ListData, TodoistResponse
from app.schemas.tasks import TaskData, TaskEditRequest

router = APIRouter(prefix="/projects/{project_uid}/tasks", tags=["Tasks"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    name="Get all tasks for a project",
)
async def get_all_tasks(
    project_uid: str,
    projects_service: ProjectServiceDep,
    tasks_service: TaskServiceDep,
    current_user: CurrentUserDep,
) -> TodoistResponse[ListData[TaskData]]:
    project = await projects_service.retrieve_project(current_user.id, project_uid)
    tasks = await tasks_service.retrieve_all_tasks(project.id)

    return TodoistResponse(
        success=True,
        data=ListData(
            count=len(tasks),
            items=[
                TaskData(
                    uid=task.uid,
                    content=task.content,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    scheduled_at=task.scheduled_at,
                    is_finished=task.is_finished,
                )
                for task in tasks
            ],
        ),
    )


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    name="Create task for a project",
)
async def create_task(
    project_uid: str,
    task_to_create: TaskEditRequest,
    tasks_service: TaskServiceDep,
    current_user: CurrentUserDep,
) -> TodoistResponse[TaskData]:
    task = await tasks_service.create(
        current_user,
        project_uid,
        task_to_create.content,
        task_to_create.is_finished,
        task_to_create.scheduled_at,
    )

    return TodoistResponse(
        success=True,
        data=TaskData(
            uid=task.uid,
            content=task.content,
            created_at=task.created_at,
            updated_at=task.updated_at,
            scheduled_at=task.scheduled_at,
            is_finished=task.is_finished,
        ),
    )


@router.get(
    "/{task_uid}", response_model_exclude_none=True, name="Get a task for a project"
)
async def get_task(
    project_uid: str,
    task_uid: str,
    tasks_service: TaskServiceDep,
    current_user: CurrentUserDep,
) -> TodoistResponse[TaskData]:
    task = await tasks_service.retrieve_task(current_user, project_uid, task_uid)

    return TodoistResponse(
        success=True,
        data=TaskData(
            uid=task.uid,
            content=task.content,
            created_at=task.created_at,
            updated_at=task.updated_at,
            scheduled_at=task.scheduled_at,
            is_finished=task.is_finished,
        ),
    )


@router.delete(
    "/{task_uid}", response_model_exclude_none=True, name="Delete task for project"
)
async def delete_task(
    project_uid: str,
    task_uid: str,
    tasks_service: TaskServiceDep,
    current_user: CurrentUserDep,
) -> TodoistResponse[TaskData]:
    task = await tasks_service.delete_task(current_user, project_uid, task_uid)

    return TodoistResponse(
        success=True,
        data=TaskData(
            uid=task.uid,
            content=task.content,
            created_at=task.created_at,
            updated_at=task.updated_at,
            scheduled_at=task.scheduled_at,
            is_finished=task.is_finished,
        ),
    )


@router.put("/{task_id}", response_model_exclude_none=True, name="tasks:update")
async def update_task(
    project_uid: str,
    task_uid: str,
    task_to_update: TaskEditRequest,
    task_service: TaskServiceDep,
    current_user: CurrentUserDep,
) -> TodoistResponse[TaskData]:
    updated_task = await task_service.update(
        current_user, project_uid, task_uid, task_to_update
    )
    return TodoistResponse(success=True, data=updated_task)
