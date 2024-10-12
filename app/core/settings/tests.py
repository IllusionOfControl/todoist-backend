from pydantic_settings import SettingsConfigDict

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    model_config = SettingsConfigDict(
        env_file=".env.tests", env_nested_delimiter="__", extra="ignore"
    )
