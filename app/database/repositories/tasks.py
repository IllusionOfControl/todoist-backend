from datetime import date, datetime

from sqlalchemy import select, insert, update, delete

from app.database.repositories.base import BaseRepository
from app.models.tasks import Task

__all__ = ["TasksRepository"]


class TasksRepository(BaseRepository):
    async def get_all_by_project(self, project_id: int) -> list[Task]:
        query = select(Task).where(Task.project_id == project_id)
        result = await self._session.scalars(query)
        return list(result)

    async def get_by_uid(self, uid: str) -> Task:
        query = select(Task).where(Task.uid == uid).limit(1)
        return await self._session.scalar(query)

    async def get_for_project_by_uid(self, project_id: int, uid: str) -> Task:
        query = select(Task).where(Task.uid == uid).where(Task.project_id == project_id).limit(1)
        return await self._session.scalar(query)

    async def create_task(
            self,
            uid: str,
            content: str,
            project_id: int,
            is_finished: bool,
            scheduled_at: date,
    ) -> Task:
        query = insert(Task).values(
            uid=uid,
            content=content,
            project_id=project_id,
            is_finished=is_finished,
            scheduled_at=scheduled_at,
        ).returning(Task)
        result = await self._session.execute(query)

        return result.scalar()

    async def update_task(
            self,
            uuid: str,
            content: str | None,
            is_finished: bool | None,
            scheduled_at: date | None,
    ):
        query = (update(Task)
                 .where(Task.uid == uuid)
                 .values(updated_at=datetime.now()))
        if content:
            query.values(content=content)
        if is_finished:
            query.values(is_finished=is_finished)
        if scheduled_at:
            query.values(scheduled_at=scheduled_at)

        result = await self._session.execute(query)
        return result.scalar()

    async def delete(self, uid) -> int:
        query = delete(Task).where(Task.uid == uid)
        result = await self._session.execute(query)
        return result.rowcount()

    # async def get_task_by_id(self, *, task_id: int) -> TaskDomain:
    #     sql = """
    #         SELECT * FROM tasks WHERE id=($1)
    #     """
    #
    #     task_row = await self.connection.fetch(
    #         sql,
    #         task_id
    #     )
    #
    #     if task_row:
    #         return TaskDomain(**dict(*task_row))
    #
    #     raise EntityDoesNotExist("task with id {0} does not exists".format(task_id))
    #
    #
    #
    #
    #
    # async def remove_project(self, *, task: TaskDomain):
    #     sql = """
    #         DELETE FROM tasks WHERE id=($1);
    #     """
    #
    #     await self.connection.fetch(
    #         sql,
    #         task.id
    #     )
    #
    # async def get_all_unfinished_tasks_by_owner_id(self, owner_id: int) -> List[TaskDomain]:
    #     sql = """
    #         SELECT * FROM tasks
    #         WHERE is_finished=FALSE AND project_id=ANY(
    #             SELECT id FROM projects WHERE owner_id=($1)
    #         );
    #     """
    #
    #     tasks_rows = await self.connection.fetch(
    #         sql,
    #         owner_id
    #     )
    #
    #     return [TaskDomain(**dict(row)) for row in tasks_rows]
    #
    # async def get_tasks_for_next_7_days(self, owner_id: int) -> List[TaskDomain]:
    #     sql = """
    #         SELECT * FROM tasks
    #         WHERE is_finished=FALSE AND
    #             scheduled_at<(current_date + 7) AND
    #             project_id=ANY(
    #             SELECT id FROM projects WHERE owner_id=($1)
    #         ) ORDER BY created_at;
    #     """
    #
    #     tasks_rows = await self.connection.fetch(
    #         sql,
    #         owner_id
    #     )
    #
    #     return [TaskDomain(**dict(row)) for row in tasks_rows]
    #
    # async def get_tasks_for_today(self, owner_id: int) -> List[TaskDomain]:
    #     sql = """
    #         SELECT * FROM tasks
    #         WHERE is_finished=FALSE AND
    #             scheduled_at=current_date AND
    #             project_id=ANY(
    #                 SELECT id FROM projects WHERE owner_id=$1
    #         ) ORDER BY created_at;
    #     """
    #
    #     tasks_rows = await self.connection.fetch(
    #         sql,
    #         owner_id
    #     )
    #
    #     return [TaskDomain(**dict(row)) for row in tasks_rows]
