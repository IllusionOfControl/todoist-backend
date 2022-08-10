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

    async def get_all_projects(self, *, user: UserDomain) -> List[ProjectDomain]:
        sql = """
            SELECT * FROM projects WHERE owner_id=($1);
        """

        projects_rows = await self.connection.fetch(
            sql,
            user.id
        )

        return [ProjectDomain(**dict(row)) for row in projects_rows]

    async def get_project(self, *, user: UserDomain, project_id) -> ProjectDomain:
        sql = """
            SELECT * FROM projects WHERE owner_id=($1) AND id=($2);
        """

        project_row = await self.connection.fetch(
            sql,
            user.id,
            project_id
        )

        if project_row:
            return ProjectDomain(**dict(project_row))

        raise EntityDoesNotExist("project does not exists")

    async def delete_project(self, *, project_id):
        sql = """
            DELETE FROM projects WHERE id=($1);
        """

        project_row = await self.connection.fetch(
            sql,
            project_id
        )

        if project_row:
            return ProjectDomain(**dict(project_row))

        raise EntityDoesNotExist("project does not exists")

    async def update_project(
        self,
        *,
        projects: ProjectDomain,
        title,
        description,
    ):
        pass
