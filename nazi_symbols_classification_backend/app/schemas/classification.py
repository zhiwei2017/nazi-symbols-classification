from pydantic import BaseModel, Field  # type: ignore
from typing import List


class ClassificationResultDetails(BaseModel):
    predicted_class: str = Field(...)
    predicted_prob: float = Field(...)


class ClassifyResponse(BaseModel):
    nazi_symbol: str = Field(...)
    prob: float = Field(...)
    details: List[ClassificationResultDetails] = Field(...)
