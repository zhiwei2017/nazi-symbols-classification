"""Configuration interface, provides a function `get_settings` to get the
used settings instance for the web service."""

import os
from functools import lru_cache
from typing import cast
from .base import Settings
from .settings_factory import SettingsFactory

# name of the environment variable, used for defining the deployment environment
# For each different deployment environment, there should be a corresponding
# settings class defined.
ENV_VAR_MODE = "MODE"

factory = SettingsFactory()
factory.register("DEFAULT", Settings)

# Add your own modes and settings here

"""
# By overriding variables in an existing BaseSettings child:
factory.register("TEST", Settings, VARIABLE_TO_OVERRIDE="override")

# By using inheritance:

class TestSettings(Settings):
    VARIABLE_TO_OVERRIDE: str = "override"

factory.register("TEST", TestSettings)
"""


@lru_cache()
def get_settings() -> Settings:
    """Get different settings objects according to different values of
    environment variable `MODE`, and use cache to speed up the execution.

    Returns:
        Settings: The instance of the current used settings class.
    """
    mode_name = os.environ.get(ENV_VAR_MODE, "DEFAULT")
    return cast(Settings, factory[mode_name])
