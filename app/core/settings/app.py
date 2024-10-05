import logging
import sys
from typing import Any, Dict, List

from loguru import logger
from pydantic import BaseModel, field_validator, PostgresDsn, SecretStr

from app.core.logging import InterceptHandler
from app.core.settings.base import BaseAppSettings


class ServerSettings(BaseModel):
    debug: bool = False
    base_url: str = 'http://localhost:8000'
    openapi_docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_spec_url: str = "/openapi.json"
    redoc_docs_url: str = "/docs"
    title: str = "application"
    version: str = "0.0.0"
    api_prefix: str = "/api"

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self,
            "docs_url": self.openapi_docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_spec_url,
            "redoc_docs_url": self.redoc_docs_url,
            "title": self.title,
            "version": self.version,
        }


class DatabaseSettings(BaseModel):
    url: PostgresDsn


class SecuritySettings(BaseModel):
    api_prefix: str = "/api"
    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = []
    secret_key: SecretStr


class LoggingSettings(BaseModel):
    level: int = logging.INFO
    logger_enable: list[str] = ["uvicorn.asgi", "uvicorn.access"]
    logger_disable: list[str] = []
    format: str = (
        "[{level: <8}] [{extra[module_name]: <9}] [{extra[request_id]: <22}] [{function}:{line}] {message}"
    )

    @field_validator("level")
    def validate_logging_level(cls, level_str: str) -> int:
        try:
            return getattr(logging, level_str.upper())
        except AttributeError:
            raise ValueError(f"Invalid logging level: {level_str}")

    def configure_logging(self) -> None:
        logger.remove()

        for logger_name in self.logger_disable:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.disabled = True

        logging.getLogger().handlers = [InterceptHandler()]  # todo ???
        for logger_name in self.logger_enable:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.level)]

        logger.configure(
            handlers=[
                {"sink": sys.stderr, "level": self.level}
            ],
            extra={"request_id": ""}
        )


class AppSettings(BaseAppSettings):
    server: ServerSettings
    database: DatabaseSettings
    security: SecuritySettings
    logging: LoggingSettings = LoggingSettings()


