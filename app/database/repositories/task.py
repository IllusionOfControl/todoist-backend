from datetime import date, datetime

from sqlalchemy import delete, insert, select, update

from app.database.repositories.base import BaseRepository
from app.models.task import Task

__all__ = ["TaskRepository"]


class TaskRepository(BaseRepository):
    async def get_all_by_project(self, project_id: int) -> list[Task]:
        query = select(Task).where(Task.project_id == project_id)
        result = await self._session.scalars(query)
        return list(result)

    async def get_by_uid(self, uid: str) -> Task:
        query = select(Task).where(Task.uid == uid).limit(1)
        return await self._session.scalar(query)

    async def get_for_project_by_uid(self, project_id: int, uid: str) -> Task:
        query = (
            select(Task)
            .where(Task.uid == uid)
            .where(Task.project_id == project_id)
            .limit(1)
        )
        return await self._session.scalar(query)

    async def create(
        self,
        uid: str,
        content: str,
        project_id: int,
        is_finished: bool,
        scheduled_at: date,
    ) -> Task:
        query = (
            insert(Task)
            .values(
                uid=uid,
                content=content,
                project_id=project_id,
                is_finished=is_finished,
                scheduled_at=scheduled_at,
            )
            .returning(Task)
        )
        result = await self._session.execute(query)

        return result.scalar()

    async def update(
        self,
        uuid: str,
        content: str | None,
        is_finished: bool | None,
        scheduled_at: date | None,
    ):
        query = (
            update(Task)
            .where(Task.uid == uuid)
            .values(content=content)
            .values(is_finished=is_finished)
            .values(updated_at=datetime.now())
        )
        if scheduled_at:
            query.values(scheduled_at=scheduled_at)

        result = await self._session.execute(query)
        return result.scalar()

    async def delete(self, uid) -> int:
        query = delete(Task).where(Task.uid == uid)
        result = await self._session.execute(query)
        return result.rowcount()
