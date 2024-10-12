import logging

from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    debug: bool = False
    title: str = "Todoist clone application"
    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
