"""Module containing FastAPI instance related functions and classes."""

import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from nazi_symbols_classification.image_processing import (
    auto_resize, grayscale, auto_adjust_contrast
)
from nazi_symbols_classification.pipeline import Pipeline
from .routes import router
from .configs import get_settings
from .middlewares.logging import log_time
from .globals import state
from .version import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    # do something before app is ready
    state["image_preprocessing_pipeline"] = Pipeline([
        ("auto_resize", auto_resize, (640, 640)),
        ("grayscale", grayscale, None),
        ("auto_adjust_contrast", auto_adjust_contrast, None),
    ])
    yield
    # do something before app is shutting down
    state.clear()


def create_application() -> FastAPI:
    """Create a FastAPI instance.

    Returns:
        object of FastAPI: the fast api application instance.
    """
    settings = get_settings()
    application = FastAPI(title=settings.PROJECT_NAME,
                          lifespan=lifespan,
                          debug=settings.DEBUG,
                          version=__version__,
                          openapi_url=f"{settings.API_STR}/openapi.json")

    # Set all CORS enabled origins
    if settings.CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           settings.CORS_ORIGINS],
            allow_origin_regex=settings.CORS_ORIGIN_REGEX,
            allow_credentials=settings.CORS_CREDENTIALS,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
        )

    # add defined routers
    application.include_router(router, prefix=settings.API_STR)

    # load logging config
    logging.config.dictConfig(settings.LOGGING_CONFIG.model_dump())
    for default_logger in ["asyncio", "uvicorn.access"]:
        logging.getLogger(default_logger).propagate = False

    # add defined middleware functions
    application.add_middleware(BaseHTTPMiddleware, dispatch=log_time)
    return application
