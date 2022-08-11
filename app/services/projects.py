from app.models.domains.users import UserDomain
from app.models.domains.projects import ProjectDomain


async def check_user_check_can_user_modify_project(project: ProjectDomain, user: UserDomain) -> bool:
    return project.owner_id == user.id
