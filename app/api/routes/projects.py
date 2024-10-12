from fastapi import APIRouter
from starlette import status

from app.api.dependencies.authentication import CurrentUser
from app.api.dependencies.services import ProjectServiceDep, TaskServiceDep
from app.schemas.projects import ProjectCreateRequest, ProjectData
from app.schemas.response import TodoistResponse, ListData
from app.schemas.tasks import TaskData

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    name="Create a new project",
)
async def create_new_project(
        create_request: ProjectCreateRequest,
        project_service: ProjectServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ProjectData]:
    project = await project_service.create_project(
        current_user.id,
        create_request.title,
        create_request.description,
        create_request.color,
    )
    return TodoistResponse(
        success=True,
        data=ProjectData(
            uid=project.uid,
            title=project.title,
            description=project.description,
            color=project.color,
            tasks=[]
        ),
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    name="Get all projects for a current user",
)
async def get_all_projects(
        project_service: ProjectServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ListData[ProjectData]]:
    projects = await project_service.retrieve_all_projects(current_user.id)

    return TodoistResponse(
        success=True,
        data=ListData(
            count=len(projects),
            items=[
                ProjectData(
                    uid=project.uid,
                    title=project.title,
                    description=project.description,
                    color=project.color,
                    tasks=[]
                ) for project in projects
            ],
        )
    )


@router.get(
    "/{project_uid}",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    name="Get a project"
)
async def get_project(
        project_uid: str,
        project_service: ProjectServiceDep,
        tasks_service: TaskServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ProjectData]:
    project = await project_service.retrieve_project(current_user.id, project_uid)
    tasks = await tasks_service.retrieve_all_tasks(project_uid)

    return TodoistResponse(
        success=True,
        data=ProjectData(
            uid=project.uid,
            title=project.title,
            description=project.description,
            color=project.color,
            tasks=[
                TaskData(
                    uid=task.uid,
                    content=task.content,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    scheduled_at=task.scheduled_at,
                    is_finished=task.is_finished,
                ) for task in tasks
            ]
        )
    )


@router.put(
    '/{project_uid}',
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    name="Update a project",
)
async def update_project_by_id(
        project_uid: str,
        project_service: ProjectServiceDep,
        tasks_service: TaskServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ProjectData]:
    project = await project_service.update_project(current_user.id, project_uid)
    tasks = await tasks_service.retrieve_all_tasks(project_uid)

    return TodoistResponse(
        success=True,
        data=ProjectData(
            uid=project.uid,
            title=project.title,
            description=project.description,
            color=project.color,
            tasks=[
                TaskData(
                    uid=task.uid,
                    content=task.content,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    scheduled_at=task.scheduled_at,
                    is_finished=task.is_finished,
                ) for task in tasks
            ]
        )
    )


@router.delete(
    '/{project_uid}',
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    name="Delete a project",
)
async def delete_project(
        project_uid: str,
        project_service: ProjectServiceDep,
        current_user: CurrentUser
) -> TodoistResponse:
    await project_service.remove_project(current_user, project_uid)
    return TodoistResponse(
        success=True,
    )
