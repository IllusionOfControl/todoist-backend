from pydantic_settings import SettingsConfigDict

from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    model_config = SettingsConfigDict(env_file=".env.debug", env_nested_delimiter="__", extra='ignore')
