"""Endpoints for health check and getting version information"""
from typing import Any
from fastapi import APIRouter
from ..schemas.system import HealthResponse, VersionResponse
from ..version import __version__

system_router = APIRouter()


@system_router.get("/health", response_model=HealthResponse)
async def health() -> Any:
    """Provide Health check endpoint function.

    \f
    Returns:
        HealthResponse: A json response containing a short message.
    """
    return HealthResponse(message="Server is healthy!")


@system_router.get("/version", response_model=VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return VersionResponse(version=__version__)
