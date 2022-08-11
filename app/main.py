from fastapi import FastAPI
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.config import get_app_settings
from app.api.routes.api import router


# TODO: Rewrite main.py
# TODO: Write tests
# TODO: Add error handling
# TODO: Add strings

settings = get_app_settings()
settings.configure_logging()

app = FastAPI(
    **settings.fastapi_kwargs
)

app.include_router(router)


app.add_event_handler(
    "startup",
    create_start_app_handler(app, settings),
)

app.add_event_handler(
    "shutdown",
    create_stop_app_handler(app, settings),
)
