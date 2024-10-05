import uuid

from app.core.exceptions import ProjectNotFoundException, ProjectPermissionException
from app.database.repositories.projects import ProjectRepository
from app.models.projects import Project


class ProjectsService:
    def __init__(
            self,
            project_repo: ProjectRepository,
    ):
        self._project_repo = project_repo

    async def create_project(self, owner_id: int, title: str, description: str, color: int) -> Project:
        project = await self._project_repo.create(
            uuid=uuid.uuid4().hex,
            title=title,
            description=description,
            owner_id=owner_id,
            color=color
        )
        return project

    async def retrieve_all_projects(self, owner_id: int) -> list[Project]:
        projects = await self._project_repo.get_all_by_owner(owner_id)
        return projects

    async def retrieve_project(self, owner_id: int, project_uid: str) -> Project:
        project = await self._project_repo.get_by_uid(project_uid)
        if project is None:
            raise ProjectNotFoundException()
        if project.owner_id != owner_id:
            raise ProjectPermissionException()

        return project

    async def remove_project(self, owner_id: int, project_uid: str) -> None:
        project = await self._project_repo.get_by_uid(project_uid)
        if project is None:
            raise ProjectNotFoundException()
        if project.owner_id != owner_id:
            raise ProjectPermissionException()

        await self._project_repo.delete(project_uid)

    async def update_project(self, owner_id, project_uid: str, title: str, description: str, color: int) -> Project:
        project = await self._project_repo.get_by_uid(project_uid)

        if project is None:
            raise ProjectNotFoundException()
        if owner_id.id != project.owner_id:
            raise ProjectPermissionException()

        project = await self._project_repo.update(project_uid, title, description, color)
        return project
