from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnvTypes, BaseAppSettings
from app.core.settings.development import DevAppSettings
from functools import lru_cache
from typing import DefaultDict, Type
from collections import defaultdict


environments: DefaultDict[AppEnvTypes, Type[AppSettings]] = defaultdict(lambda: AppSettings, {
    AppEnvTypes.dev: DevAppSettings,
})


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
