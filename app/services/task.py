import uuid
from datetime import date

from app.core.exceptions import TaskNotFoundException
from app.database.repositories.task import TaskRepository
from app.models.task import Task
from app.models.user import User
from app.schemas.tasks import TaskData
from app.services.project import ProjectService


class TaskService:
    def __init__(
        self, projects_service: ProjectService, tasks_repository: TaskRepository
    ):
        self._projects_service = projects_service
        self._tasks_repository = tasks_repository

    async def create_task(
        self,
        current_user: User,
        project_uid: str,
        content: str,
        is_finished: bool,
        scheduled_at: date | None,
    ) -> TaskData:
        project = await self._projects_service.retrieve_project(
            current_user.id, project_uid
        )

        task = await self._tasks_repository.create(
            uuid.uuid4().hex, content, project.id, is_finished, scheduled_at
        )
        return TaskData(
            content=task.content,
            uid=task.uid,
            is_finished=task.is_finished,
            scheduled_at=task.scheduled_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def retrieve_all_tasks(
        self, current_user: User, project_uid: str
    ) -> list[Task]:
        project = await self._projects_service.retrieve_project(
            current_user.id, project_uid
        )
        tasks = await self._tasks_repository.get_all_by_project(project.id)
        return tasks

    async def retrieve_task(
        self, current_user: User, project_uid: str, task_uid: str
    ) -> Task:
        project = await self._projects_service.retrieve_project(
            current_user.id, project_uid
        )
        task = await self._tasks_repository.get_for_project_by_uid(project.id, task_uid)
        return task

    async def update_task(
        self,
        current_user: User,
        project_uid: str,
        task_uid: str,
        content: str | None,
        is_finished: str | None,
        scheduled_at: date | None,
    ) -> Task:
        project = await self._projects_service.retrieve_project(
            current_user.id, project_uid
        )
        task = await self._tasks_repository.get_for_project_by_uid(project.id, task_uid)
        if not task:
            raise TaskNotFoundException()

        task = await self._tasks_repository.update(
            task.uid, content, is_finished, scheduled_at
        )

        return task

    async def delete_task(
        self, current_user: User, project_uid: str, task_uid: str
    ) -> Task:
        project = await self._projects_service.retrieve_project(
            current_user.id, project_uid
        )
        task = await self._tasks_repository.get_for_project_by_uid(project.id, task_uid)
        if not task:
            raise TaskNotFoundException()

        return task

    async def get_task(
        self, current_user: User, project_uid: str, task_uid: str
    ) -> Task:
        project = await self._projects_service.retrieve_project(
            current_user.id, project_uid
        )
        task = await self._tasks_repository.get_for_project_by_uid(project.id, task_uid)

        if not task:
            raise TaskNotFoundException()

        return task
