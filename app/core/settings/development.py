from app.core.settings.app import AppSettings
import logging


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Todoist clone application"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
