from app.models.users import User
from app.models.projects import ProjectDomain


async def check_can_user_modify_project(project: ProjectDomain, user: User) -> bool:
    return project.owner_id == user.id
