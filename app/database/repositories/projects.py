from datetime import datetime

from sqlalchemy import insert, select, update, delete

from app.database.repositories.base import BaseRepository
from app.models.projects import Project
from app.models.tasks import Task


class ProjectRepository(BaseRepository):
    async def create(
            self,
            uuid: str,
            title: str,
            description: str,
            owner_id: int,
            color: int
    ) -> Project:
        query = insert(Project).values(
            uid=uuid,
            title=title,
            description=description,
            owner_id=owner_id,
            color=color,
        ).returning(Project)

        result = await self._session.execute(query)
        return result.scalar()

    async def get_by_uid(self, uid: str) -> Project:
        query = select(Project).where(Project.uid == uid)
        return await self._session.scalar(query)

    async def get_all_by_owner(self, owner_id: int) -> list[Project]:
        query = select(Project).where(Project.owner_id == owner_id)
        result = await self._session.execute(query)
        return list(result.scalars())

    async def update(
            self,
            uid: str,
            title: str,
            description: str,
            color: int,
    ) -> Project:
        query = update(Project).where(Task.uid == uid).values(
            updated_at=datetime.now()
        ).returning(Project)

        if title:
            query.values(title=title)
        if description is not None:
            query.values(description=description)
        if color is not None:
            query.values(color=color)

        result = await self._session.execute(query)

        return result.scalar()

    async def delete(self, uid: str) -> int:
        query = delete(Project).where(uid=uid)
        result = await self._session.execute(query)
        return result.rowcount()
