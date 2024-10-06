import uuid
from datetime import date

from app.core.exceptions import TaskNotFoundException
from app.database.repositories.tasks import TasksRepository
from app.models.tasks import Task
from app.schemas.tasks import TaskData


class TaskService:
    def __init__(self, tasks_repository: TasksRepository):
        self._tasks_repository = tasks_repository

    async def create_task(self, project_id: int, content: str, is_finished: bool,
                          scheduled_at: date | None) -> TaskData:

        task = await self._tasks_repository.create_task(
            uuid.uuid4().hex,
            content,
            project_id,
            is_finished,
            scheduled_at,
        )
        return TaskData(
            content=task.content,
            uid=task.uid,
            is_finished=task.is_finished,
            scheduled_at=task.scheduled_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def retrieve_all_tasks(self, project_id: int) -> list[Task]:
        tasks = await self._tasks_repository.get_all_by_project(project_id)
        return tasks

    async def retrieve_task(self, project_id: int, task_uid: str) -> Task:
        task = await self._tasks_repository.get_for_project_by_uid(project_id, task_uid)
        return task

    async def update_task(self, project_id: int, task_uid: str, content: str | None, is_finished: str | None,
                          scheduled_at: date | None) -> Task:
        task = await self._tasks_repository.get_for_project_by_uid(project_id, task_uid)
        if not task:
            raise TaskNotFoundException()

        task = await self._tasks_repository.update_task(
            task.uid,
            content,
            is_finished,
            scheduled_at,
        )

        return task

    async def delete_task(self, project_id: int, task_uid: str) -> Task:
        task = await self._tasks_repository.get_for_project_by_uid(project_id, task_uid)
        if not task:
            raise TaskNotFoundException()

        return task

    async def get_task(self, project_id: int, task_uid: str) -> Task:
        task = await self._tasks_repository.get_for_project_by_uid(project_id, task_uid)

        if not task:
            raise TaskNotFoundException()

        return task
