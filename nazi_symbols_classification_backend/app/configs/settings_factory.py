from pydantic_settings import BaseSettings
from typing import Dict, List, Tuple, Type


class SettingsFactory:
    """Factory used to create different Settings or configurations."""

    def __init__(self) -> None:
        self._settings: Dict[str, Tuple[Type[BaseSettings], Dict]] = {}

    def register(self, mode: str, settings_class: Type[BaseSettings], **kwargs) -> None:
        """This method will associate a BaseSettings class with a particular mode. If the provided
        mode already exists, it will be overrided.

        Additional kwargs will be passed on to BaseSettings class to build settings object.

        Args:
            mode (str): String representing a deployment mode (DEV, TEST, PROD, ...).
            settings_class (Type[BaseSettings]):  BaseSettings class associated with given mode.
        """
        self._settings[mode] = (settings_class, kwargs or {})

    def modes(self) -> List[str]:
        """Returns a list of  available modes.

        Returns:
            List[str]: List of available modes.
        """
        return list(self._settings.keys())

    def __getitem__(self, mode: str) -> BaseSettings:
        settings_tuple = self._settings.get(mode, None)
        if not settings_tuple:
            raise ValueError(f"Mode [{mode}] not registered in settings.")

        settings_class, params = settings_tuple
        return settings_class(**params)
