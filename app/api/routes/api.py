from fastapi import APIRouter
from app.api.routes import authentication, projects


router = APIRouter()


router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(projects.router, tags=["projects"], prefix="/projects")
