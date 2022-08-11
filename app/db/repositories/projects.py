from app.db.repositories.base import BaseRepository
from app.db.errors import EntityDoesNotExist
from app.models.domains.users import UserDomain
from app.models.domains.projects import ProjectDomain
from typing import List


class ProjectsRepository(BaseRepository):
    async def create_project(
        self,
        *,
        title: str,
        user: UserDomain
    ) -> ProjectDomain:
        sql = """
            INSERT INTO projects (title, owner_id) 
            VALUES (($1), ($2)) 
            RETURNING *;
        """

        project_row = await self.connection.fetch(
            sql,
            title,
            user.id
        )

        return ProjectDomain(**dict(*project_row))

    async def get_all_projects_by_user(self, *, user: UserDomain) -> List[ProjectDomain]:
        sql = """
            SELECT * FROM projects WHERE owner_id=($1);
        """

        projects_rows = await self.connection.fetch(
            sql,
            user.id
        )

        return [ProjectDomain(**dict(row)) for row in projects_rows]

    async def get_project_by_id(self, *, project_id: int) -> ProjectDomain:
        sql = """
            SELECT * FROM projects WHERE id=($1);
        """

        project_row = await self.connection.fetch(
            sql,
            project_id
        )

        if project_row:
            return ProjectDomain(**dict(*project_row))

        raise EntityDoesNotExist("project does not exists")

    async def update_project(
        self,
        *,
        project: ProjectDomain,
        title,
        description,
    ):
        sql = """
            UPDATE projects
            SET title=($2), description=($3), updated_at=now()
            WHERE id=($1)
            RETURNING updated_at;
        """

        updated_project = project.copy(deep=True)
        updated_project.title = title or project.title
        updated_project.description = description or project.description

        updated_project.updated_at = await self.connection.fetch(
            sql,
            project.id,
            updated_project.title,
            updated_project.description
        )

        return updated_project

    async def remove_project(self, *, project: ProjectDomain):
        sql = """
            DELETE FROM projects WHERE id=($1);
        """

        await self.connection.fetch(
            sql,
            project.id
        )
