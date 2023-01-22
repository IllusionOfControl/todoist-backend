from fastapi import APIRouter, Depends, Body, Response, HTTPException
from starlette import status
from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.projects import get_project_by_id_from_path, check_project_ownership
from app.api.dependencies.database import get_repository
from app.db.repositories.projects import ProjectsRepository
from app.models.domains.users import UserDomain
from app.models.domains.projects import ProjectDomain
from app.models.schemas.projects import ProjectInCreate, ProjectInResponse, ListOfProjectsInResponse, ProjectInUpdate
from app.resourses import strings
from app.db.errors import EntityDoesNotExist

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectInResponse,
    name="projects:create-project"
)
async def create_new_project(
    project_create: ProjectInCreate = Body(...),
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer())
) -> ProjectInResponse:
    try:
        if await project_repo.get_project_by_title(title=project_create.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=strings.PROJECT_ALREADY_EXISTS,
            )
    except EntityDoesNotExist:
        pass

    project = await project_repo.create_project(title=project_create.title, owner_id=user.id)

    return ProjectInResponse(**project.dict())


@router.get(
    "",
    response_model=ListOfProjectsInResponse,
    name="projects:list-project"
)
async def list_projects(
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    user: UserDomain = Depends(get_current_user_authorizer())
) -> ListOfProjectsInResponse:
    projects = await project_repo.get_all_projects_by_owner_id(owner_id=user.id)

    projects_for_response = [
        ProjectInResponse(**project.dict()) for project in projects
    ]

    return ListOfProjectsInResponse(
        projects=projects_for_response,
        count=len(projects_for_response)
    )


@router.get(
    '/{project_id}',
    response_model=ProjectInResponse,
    name="projects:get-project",
    dependencies=[Depends(check_project_ownership)]
)
async def retrieve_project_by_id(
    project: ProjectDomain = Depends(get_project_by_id_from_path),
) -> ProjectInResponse:
    return ProjectInResponse(**project.dict())


@router.put(
    '/{project_id}',
    response_model=ProjectInResponse,
    name="project:update-project",
    dependencies=[Depends(check_project_ownership)]
)
async def update_project_by_id(
    project_update: ProjectInUpdate = Body(...),
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository)),
    project: ProjectDomain = Depends(get_project_by_id_from_path),
) -> ProjectInResponse:
    new_project = await project_repo.update_project(
        project=project,
        **project_update.dict()
    )

    return ProjectInResponse(**new_project.dict())


@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    name="project:remove-project",
    dependencies=[Depends(check_project_ownership)],
    response_class=Response
)
async def remove_project(
    project: ProjectDomain = Depends(get_project_by_id_from_path),
    project_repo: ProjectsRepository = Depends(get_repository(ProjectsRepository))
) -> None:
    await project_repo.remove_project(project=project)
