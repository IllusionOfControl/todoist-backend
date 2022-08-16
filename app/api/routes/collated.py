from fastapi import APIRouter, Depends
from app.models.schemas.tasks import TaskInResponse, ListOfTasksInResponse
from app.models.domains.users import UserDomain
from app.db.repositories.tasks import TaskRepository
from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get(
    "/inbox",
    response_model=ListOfTasksInResponse,
)
async def list_unfinished_tasks(
    current_user: UserDomain = Depends(get_current_user_authorizer()),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> ListOfTasksInResponse:
    tasks = await task_repo.get_all_unfinished_tasks_by_user(current_user)

    tasks_for_response = [
        TaskInResponse(**task.dict()) for task in tasks
    ]

    return ListOfTasksInResponse(
        tasks=tasks_for_response,
        count=len(tasks_for_response)
    )


@router.get(
    "/next_7",
    response_model=ListOfTasksInResponse,
)
async def list_unfinished_tasks_for_next_7_days(
    current_user: UserDomain = Depends(get_current_user_authorizer()),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> ListOfTasksInResponse:
    tasks = await task_repo.get_tasks_for_next_7_days(current_user)

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
async def list_unfinished_tasks_for_next_7_days(
    current_user: UserDomain = Depends(get_current_user_authorizer()),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> ListOfTasksInResponse:
    tasks = await task_repo.get_tasks_for_today(current_user)

    tasks_for_response = [
        TaskInResponse(**task.dict()) for task in tasks
    ]

    return ListOfTasksInResponse(
        tasks=tasks_for_response,
        count=len(tasks_for_response)
    )
