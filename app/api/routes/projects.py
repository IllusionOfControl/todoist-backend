from fastapi import APIRouter
from starlette import status

from app.api.dependencies.authentication import CurrentUser
from app.api.dependencies.services import ProjectsServiceDep, TasksServiceDep
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
    response_model=TodoistResponse[ProjectData],
    name="projects:create-project"
)
async def create_new_project(
        create_request: ProjectCreateRequest,
        project_repo: ProjectsServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ProjectData]:
    project = project_repo.create_project(
        current_user.id,
        create_request.title,
        create_request.description,
        create_request.color,
    )
    return TodoistResponse[ProjectData](
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
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoistResponse[ProjectData],
    name="projects:get_all_projects"
)
async def get_all_projects(
        project_repo: ProjectsServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ListData[ProjectData]]:
    projects = await project_repo.retrieve_all_projects(current_user.id)

    return TodoistResponse[ListData[ProjectData]](
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
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoistResponse[ProjectData],
    name="projects:get-project"
)
async def get_project(
        project_id: str,
        project_service: ProjectsServiceDep,
        tasks_service: TasksServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ProjectData]:
    project = await project_service.retrieve_project(current_user.id, project_id)
    tasks = await tasks_service.retrieve_all_tasks(project_id)

    return TodoistResponse[ProjectData](
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
    '/{project_id}',
    status_code=status.HTTP_200_OK,
    response_model=TodoistResponse[ProjectData],
    name="project:update-project",
)
async def update_project_by_id(
        project_id: str,
        project_service: ProjectsServiceDep,
        tasks_service: TasksServiceDep,
        current_user: CurrentUser
) -> TodoistResponse[ProjectData]:
    project = await project_service.update_project(current_user.id, project_id)
    tasks = await tasks_service.retrieve_all_tasks(project_id)

    return TodoistResponse[ProjectData](
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
    '/{project_id}',
    status_code=status.HTTP_200_OK,
    name="project:delete-project",
    response_model=TodoistResponse
)
async def delete_project(
        project_id: str,
        project_service: ProjectsServiceDep,
        current_user: CurrentUser
) -> TodoistResponse:
    await project_service.remove_project(current_user, project_id)
    return TodoistResponse(
        success=True,
    )
