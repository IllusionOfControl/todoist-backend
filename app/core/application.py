from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.routes.api import router as api_router
from app.core.config import get_app_settings
from app.database import database


class Application:
    def __init__(self):
        self._settings = get_app_settings()
        self._settings.logging.configure_logging()

        self._app = FastAPI(
            lifespan=self.lifespan
        )

        self.configure_middlewares()
        self.configure_routes()

    def configure_middlewares(self):
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=self._settings.security.allowed_hosts,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def configure_routes(self):
        self._app.include_router(api_router, prefix=self._settings.server.api_prefix)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        logger.info(
            f"Starting Application {self._settings.server.title} {self._settings.server.version}"
        )

        database.connect(self._settings.database)

        logger.info(f"Server Url: {self._settings.server.base_url}")
        logger.info(f"Docs Url: {self._settings.server.base_url}{self._settings.server.docs_url}")

        yield

        database.close()

        logger.info(
            f"Stopping Application {self._settings.server.title} {self._settings.server.version}"
        )

    @property
    def fastapi_app(self) -> FastAPI:
        return self._app