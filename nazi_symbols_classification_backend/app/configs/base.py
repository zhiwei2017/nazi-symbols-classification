"""Base settings class contains only important fields."""

# mypy: ignore-errors
import ast
import secrets
from typing import List, Union, Dict
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..utils.logging import StandardFormatter, ColorFormatter


class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = False
    formatters: Dict
    handlers: Dict
    loggers: Dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PROJECT_NAME: str = 'Nazi Symbolc Classification Backend'
    PROJECT_SLUG: str = 'nazi_symbols_classification_backend'

    DEBUG: bool = True
    API_STR: str = "/api/v1"

    # ##################### Access Token Configuration #########################
    # Please note that, the secret key will be different for each running
    # instance or each time restart the service, if you prefer a stable one,
    # please use an environment variable.
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 60 minutes * 24 hours * 30 * 6  months = 6 months
    ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN: int = 60 * 24 * 30 * 6
    JWT_ENCODE_ALGORITHM: str = "HS256"

    # ########################### CORS Configuration ###########################
    """CORS_ORIGINS is a JSON-formatted list of origins
    e.g: ["http://localhost", "http://localhost:4200", "http://localhost:3000",
    "http://localhost:8080"]"""
    CORS_ORIGINS: Union[List[str], str] = []
    """A regex string to match against origins that should be permitted to make
    cross-origin requests."""
    CORS_ORIGIN_REGEX: str = r""
    """A list of HTTP methods that should be allowed for cross-origin requests.
    Defaults to ['*']. You can use ['GET'] to allow standard GET method."""
    CORS_METHODS: List[str] = ["GET"]
    """A list of HTTP request headers that should be supported for cross-origin
    requests. Defaults to ['*'] to allow all headers. """
    CORS_HEADERS: List[str] = []
    """ Indicate that cookies should be supported for cross-origin requests.
    Defaults to True."""
    CORS_CREDENTIALS: bool = True

    # noinspection PyMethodParameters
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate the value of BACKEND_CORS_ORIGINS.

        Args:
            v (Union[str, List[str]): the value of BACKEND_CORS_ORIGINS.

        Returns:
            A list of urls, if v is a list of str in string format.
            The given value v, if v is a list or string.

        Raises
            ValueError, if v is in other format.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("[") and v.endswith("]"):
            return ast.literal_eval(v)
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # ######################## Logging Configuration ###########################
    # logging configuration for the project logger, uvicorn loggers
    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colorFormatter": {"()": ColorFormatter},
            "standardFormatter": {"()": StandardFormatter},
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standardFormatter",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "nazi_symbols_classification_backend": {
                "handlers": ["consoleHandler"],
                "level": "DEBUG",
            },
            "uvicorn": {"handlers": ["consoleHandler"]},
            "uvicorn.access": {
                # disable uvicorn.access logger, because the project logger is
                #  used to replace uvicorn.access
                "handlers": []
            },
        },
    }
