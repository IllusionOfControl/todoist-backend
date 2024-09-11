import uuid
from datetime import date

from app.database.repositories.tasks import TasksRepository
from app.models.projects import Project
from app.models.tasks import Task
from app.models.users import User
from app.schemas.tasks import TaskData


class TasksService:
    def __init__(self, tasks_repository: TasksRepository, current_user: User):
        self._tasks_repository = tasks_repository
        self._current_user = current_user

    async def create_task(self, project: Project, content: str,
                          scheduled_at: date) -> TaskData:
        if project.owner_id != self._current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        task = await self._tasks_repository.create_task(
            uuid.uuid4().hex,
            content,
            project.id,
            scheduled_at,
            self._current_user.id
        )
        return TaskData(
            content=task.content,
            uid=task.uid,
            is_finished=task.is_finished,
            scheduled_at=task.scheduled_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def update_task(self, task: Task, content: str,
                          scheduled_at: date, is_finished: bool) -> TaskData:
        if task.owner_id != self._current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        task = await self._tasks_repository.update_task(
            task.uid,
            content,
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

    async def delete_task(self, task: Task) -> bool:
        if task.owner_id != self._current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        return bool(await self._tasks_repository.delete(task.uid))

    async def list_tasks(self, project: Project) -> list[TaskData]:
        if project.owner_id != self._current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        tasks = await self._tasks_repository.get_all_by_project(
            project.id
        )

        return [
            TaskData(
                content=task.content,
                uid=task.uid,
                is_finished=task.is_finished,
                scheduled_at=task.scheduled_at,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks
        ]
