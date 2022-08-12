from fastapi import APIRouter, Body, Depends, Response
from starlette import status
from app.models.schemas.tasks import TaskInResponse, TaskInCreate, ListOfTasksInResponse, TaskInUpdate
from app.models.domains.tasks import TaskDomain
from app.db.repositories.tasks import TaskRepository
from app.api.dependencies.projects import get_project_by_id_from_path, check_project_ownership
from app.api.dependencies.tasks import get_task_by_id_from_path
from app.api.dependencies.authentication import get_current_user_authorizer
from app.models.domains.projects import ProjectDomain
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskInResponse,
    name="tasks:create_task",
    dependencies=[Depends(check_project_ownership)]
)
async def create_new_task(
    task_create: TaskInCreate = Body(...),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    project: ProjectDomain = Depends(get_project_by_id_from_path)
) -> TaskInResponse:
    task = await task_repo.create_task(title=task_create.title, project=project)

    return TaskInResponse(**task.dict())


@router.get(
    "",
    response_model=ListOfTasksInResponse,
    name="tasks:list-tasks",
    dependencies=[Depends(get_current_user_authorizer())]
)
async def list_projects(
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    project: ProjectDomain = Depends(get_project_by_id_from_path)
) -> ListOfTasksInResponse:
    projects = await task_repo.get_all_tasks_by_project(project=project)

    tasks_for_response = [
        TaskInResponse(**project.dict()) for project in projects
    ]

    return ListOfTasksInResponse(
        projects=tasks_for_response,
        count=len(tasks_for_response)
    )


@router.get(
    '/{task_id}',
    response_model=TaskInResponse,
    name="tasks:get-task",
    dependencies=[Depends(check_project_ownership)]
)
async def retrieve_task_by_id(
    task: TaskDomain = Depends(get_task_by_id_from_path)
) -> TaskInResponse:
    return TaskInResponse(**task.dict())


@router.put(
    '/{task_id}',
    response_model=TaskInResponse,
    name="tasks:update-task",
    dependencies=[Depends(check_project_ownership)]
)
async def update_task_by_id(
    task_update: TaskInUpdate = Body(...),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    task: TaskDomain = Depends(get_task_by_id_from_path)
) -> TaskInResponse:
    new_project = await task_repo.update_task(
        task=task,
        **task_update.dict()
    )

    return TaskInResponse(**new_project.dict())


@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    name="task:remove-task",
    dependencies=[Depends(check_project_ownership)],
    response_class=Response
)
async def remove_project(
    task: TaskDomain = Depends(get_task_by_id_from_path),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> None:
    await task_repo.remove_project(task=task)
