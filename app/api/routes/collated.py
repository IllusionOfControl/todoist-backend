from fastapi import APIRouter, Depends
from app.schemas import TaskInResponse, ListOfTasksInResponse
from app.models.users import User
from app.database.repositories.tasks import TasksRepository
from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get(
    "/inbox",
    response_model=ListOfTasksInResponse,
)
async def list_unfinished_tasks(
    current_user: User = Depends(get_current_user_authorizer()),
    task_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> ListOfTasksInResponse:
    tasks = await task_repo.get_all_unfinished_tasks_by_owner_id(owner_id=current_user.id)

    tasks_for_response = [
        TaskInResponse(**task.dict()) for task in tasks
    ]

    return ListOfTasksInResponse(
        tasks=tasks_for_response,
        count=len(tasks_for_response)
    )


@router.get(
    "/next7",
    response_model=ListOfTasksInResponse,
)
async def list_unfinished_tasks_for_next_7_days(
    current_user: User = Depends(get_current_user_authorizer()),
    task_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> ListOfTasksInResponse:
    tasks = await task_repo.get_tasks_for_next_7_days(owner_id=current_user.id)

    tasks_for_response = [
        TaskInResponse(**task.dict()) for task in tasks
    ]

    return ListOfTasksInResponse(
        tasks=tasks_for_response,
        count=len(tasks_for_response)
    )


@router.get(
    "/today",
    response_model=ListOfTasksInResponse,
)
async def list_unfinished_tasks_for_today(
    current_user: User = Depends(get_current_user_authorizer()),
    task_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> ListOfTasksInResponse:
    tasks = await task_repo.get_tasks_for_today(owner_id=current_user.id)

    tasks_for_response = [
        TaskInResponse(**task.dict()) for task in tasks
    ]

    return ListOfTasksInResponse(
        tasks=tasks_for_response,
        count=len(tasks_for_response)
    )
