from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.config import get_app_settings
from app.api.routes.api import router


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    application = FastAPI(
        **settings.fastapi_kwargs
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )

    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application, settings),
    )

    application.include_router(router, prefix=settings.api_prefix)

    return application


app = get_application()
