from fastapi import APIRouter

from app.api.routes import authentication, projects, tasks  # collated

api_router = APIRouter()

api_router.include_router(authentication.router)
api_router.include_router(projects.router)
api_router.include_router(tasks.router)
# router.include_router(collated.router, tags=["collated"], prefix="/collated")
