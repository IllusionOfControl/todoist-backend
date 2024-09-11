from datetime import date, datetime

from sqlalchemy import select, insert, update, delete

from app.database.repositories.base import BaseRepository
from app.models.tasks import Task


class TasksRepository(BaseRepository):
    async def get_all_by_project(self, project_id: int) -> list[Task]:
        query = select(Task).where(Task.project_id == project_id)
        result = await self._session.scalars(query)
        return list(result)

    async def create_task(
            self,
            uuid: str,
            content: str,
            project_id: int,
            scheduled_at: date,
            owner_id: int,
    ) -> Task:
        query = insert(Task).values(
            uuid=uuid,
            content=content,
            project_id=project_id,
            scheduled_at=scheduled_at,
            owner_id=owner_id
        ).returning(Task)
        result = await self._session.execute(query)

        return result.scalar()

    async def update_task(
            self,
            uuid: str,
            content: str,
            is_finished: bool,
            scheduled_at: date,
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
