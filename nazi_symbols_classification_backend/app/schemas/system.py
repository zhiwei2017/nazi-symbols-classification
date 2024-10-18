"""Define response model for the endpoint health and version."""

from pydantic import BaseModel, Field  # type: ignore


class HealthResponse(BaseModel):
    """Response for health checking endpoint."""

    message: str = Field(..., examples=["Server is healthy!"])


class VersionResponse(BaseModel):
    """Response for version endpoint."""

    version: str = Field(..., examples=["1.0.0"])
