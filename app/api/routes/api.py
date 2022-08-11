from fastapi import APIRouter
from app.api.routes import authentication, projects, tasks


router = APIRouter()


router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(projects.router, tags=["projects"], prefix="/projects")
router.include_router(tasks.router, tags=["tasks"], prefix="/projects/{project_id}/tasks")

