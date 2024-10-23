from pydantic import BaseModel, Field  # type: ignore
from typing import List


class ImageClassificationResultDetails(BaseModel):
    label: str = Field(...)
    prob: float = Field(...)


class ImageClassificationResult(BaseModel):
    containing_nazi_symbols: bool = Field(...)
    prob: float = Field(...)
    nazi_symbols: List[str] = Field(...)
    details: List[ImageClassificationResultDetails] = Field(...)


class ClassifyResponse(BaseModel):
    results: List[ImageClassificationResult] = Field(...)
