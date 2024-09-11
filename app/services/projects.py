import uuid

from app.database.repositories.projects import ProjectsRepository
from app.models.projects import Project
from app.models.users import User
from app.schemas.projects import ProjectData, ProjectInfo
from app.services.tasks import TasksService


class ProjectService:
    def __init__(
            self,
            project_repo: ProjectsRepository,
            task_service: TasksService,
            current_user: User,
    ):
        self._project_repo = project_repo
        self._tasks_service = task_service
        self._current_user = current_user

    async def create_project(self, title: str, description: str) -> ProjectData:
        project = await self._project_repo.create(
            uuid=uuid.uuid4().hex,
            title=title,
            description=description,
            owner_id=self._current_user.id
        )
        return ProjectData(
            uid=project.uuid,
            title=project.title,
            description=project.description,
            color=project.color,
            tasks=[],
        )

    async def update_project(self, project_uid: str, title: str, description: str, color: int) -> ProjectData:
        project = self._project_repo.get_by_uid(project_uid)

        if project is None:
            raise Exception()  # todo project not found
        if self._current_user.id != self._current_user.id:
            pass
            # todo project access exception

        project = await self._project_repo.update(project_uid, title, description, color)
        tasks = await self._tasks_service.list_tasks(project)
        return ProjectData(
            uid=project.uuid,
            title=project.title,
            description=project.description,
            color=project.color,
            tasks=tasks,
        )

    async def retrieve_projects(self) -> list[ProjectInfo]:
        projects = await self._project_repo.get_all_by_owner(self._current_user.id)
        return [
            ProjectInfo(
                uid=project.uuid,
                title=project.title,
                description=project.description,
                color=project.color,
            )
            for project in projects
        ]

    async def retrieve_project(self, project_uid: str) -> ProjectData:
        project = await self._project_repo.get_by_uid(project_uid)
        tasks = await self._tasks_service.list_tasks(project)

        return ProjectData(
            uid=project.uuid,
            title=project.title,
            description=project.description,
            color=project.color,
            tasks=tasks,
        )
