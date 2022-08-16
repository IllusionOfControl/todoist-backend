from app.db.repositories.base import BaseRepository
from app.db.errors import EntityDoesNotExist
from app.models.domains.tasks import TaskDomain
from app.models.domains.projects import ProjectDomain
from app.models.domains.users import UserDomain
from typing import List
from datetime import date


class TaskRepository(BaseRepository):
    async def create_task(
            self,
            *,
            title: str,
            project: ProjectDomain
    ) -> TaskDomain:
        sql = """
            INSERT INTO tasks (title, project_id)
            VALUES (($1), ($2))
            RETURNING *;
        """

        task_row = await self.connection.fetch(
            sql,
            title,
            project.id
        )

        return TaskDomain(**dict(*task_row))

    async def get_task_by_id(self, *, task_id: int) -> TaskDomain:
        sql = """
            SELECT * FROM tasks WHERE id=($1)
        """

        task_row = await self.connection.fetch(
            sql,
            task_id
        )

        if task_row:
            return TaskDomain(**dict(*task_row))

        raise EntityDoesNotExist("task with id {0} does not exists".format(task_id))

    async def get_all_tasks_by_project(self, *, project: ProjectDomain) -> List[TaskDomain]:
        sql = """
            SELECT * FROM tasks WHERE project_id=($1);
        """

        tasks_rows = await self.connection.fetch(
            sql,
            project.id
        )

        return [TaskDomain(**dict(row)) for row in tasks_rows]

    async def update_task(
        self,
        *,
        task: TaskDomain,
        title,
        scheduled_at: date,
    ):
        sql = """
            UPDATE tasks
            SET title=($2), scheduled_at=($3), updated_at=now()
            WHERE id=($1)
            RETURNING updated_at;
        """

        updated_task = task.copy(deep=True)
        updated_task.title = title or task.title
        updated_task.scheduled_at = scheduled_at or task.scheduled_at

        updated_task.updated_at = await self.connection.fetch(
            sql,
            task.id,
            updated_task.title,
            updated_task.scheduled_at
        )

        return updated_task

    async def remove_project(self, *, task: TaskDomain):
        sql = """
            DELETE FROM tasks WHERE id=($1);
        """

        await self.connection.fetch(
            sql,
            task.id
        )

    async def get_all_unfinished_tasks_by_user(self, user: UserDomain) -> List[TaskDomain]:
        sql = """
            SELECT * FROM tasks 
            WHERE is_finished=FALSE AND project_id=ANY(
                SELECT id FROM projects WHERE owner_id=($1)
            );
        """

        tasks_rows = await self.connection.fetch(
            sql,
            user.id
        )

        return [TaskDomain(**dict(row)) for row in tasks_rows]

    async def get_tasks_for_next_7_days(self, user: UserDomain) -> List[TaskDomain]:
        sql = """
            SELECT * FROM tasks 
            WHERE is_finished=FALSE AND
                scheduled_at<(current_date + 7) AND
                project_id=ANY(
                SELECT id FROM projects WHERE owner_id=($1)
            ) ORDER BY created_at;
        """

        tasks_rows = await self.connection.fetch(
            sql,
            user.id
        )

        return [TaskDomain(**dict(row)) for row in tasks_rows]

    async def get_tasks_for_today(self, user: UserDomain) -> List[TaskDomain]:
        sql = """
            SELECT * FROM tasks 
            WHERE is_finished=FALSE AND
                scheduled_at=current_date AND
                project_id=ANY(
                    SELECT id FROM projects WHERE owner_id=($1)
            ) ORDER BY created_at;
        """

        tasks_rows = await self.connection.fetch(
            sql,
            user.id
        )

        return [TaskDomain(**dict(row)) for row in tasks_rows]
