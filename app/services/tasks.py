import uuid
from datetime import date

from app.database.repositories.tasks import TasksRepository
from app.models.projects import Project
from app.models.users import User
from app.schemas.tasks import TaskData, TaskToUpdate


class TasksService:
    def __init__(self, tasks_repository: TasksRepository):
        self._tasks_repository = tasks_repository

    async def create_task(self, current_user: User, project: Project, content: str,
                          scheduled_at: date) -> TaskData:
        if project.owner_id != current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        task = await self._tasks_repository.create_task(
            uuid.uuid4().hex,
            content,
            project.id,
            scheduled_at,
            current_user.id
        )
        return TaskData(
            content=task.content,
            uid=task.uid,
            is_finished=task.is_finished,
            scheduled_at=task.scheduled_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def update_task(self, current_user: User, task_uid: str, task_to_update: TaskToUpdate) -> TaskData:
        task = await self._tasks_repository.get_by_uid(task_uid)
        if task.owner_id != current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        task = await self._tasks_repository.update_task(
            task.uid,
            task_to_update.content,
            task.is_finished,
            task.scheduled_at,
        )

        return TaskData(
            content=task.content,
            uid=task.uid,
            is_finished=task.is_finished,
            scheduled_at=task.scheduled_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def delete_task(self, current_user: User, task_uid: str) -> bool:
        task = await self._tasks_repository.get_by_uid(task_uid)
        if task.owner_id != current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        return bool(await self._tasks_repository.delete(task_uid))

    async def get_task(self, current_user: User, task_uid: str) -> TaskData:
        task = await self._tasks_repository.get_by_uid(task_uid)

        if task.owner_id != current_user.id:
            raise Exception()  # todo создать taskpermissionexception

        return TaskData(
            content=task.content,
            uid=task.uid,
            is_finished=task.is_finished,
            scheduled_at=task.scheduled_at,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )

    async def list_tasks(self, current_user: User, project: Project) -> list[TaskData]:
        if project.owner_id != current_user.id:
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
