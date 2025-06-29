from pydantic import BaseModel, Field  # type: ignore
from typing import List, Optional


class ImageClassificationResultDetails(BaseModel):
    label: str = Field(...,
                       description="Predicted nazi symbol class label",
                       examples=["Black Sun",
                                 "Flash and circle",
                                 "Broken Sun Cross",
                                 "The Happy Merchant",
                                 "Hitler",
                                 "Nazi salute",
                                 "Yellow badge",
                                 "neo-Nazi",
                                 "Siegrune",
                                 "SS Skull",
                                 "Sturmabteilung emblem",
                                 "Swastika",
                                 "Wolfsangel"])
    prob: Optional[float] = Field(None,
                                  description="Probability of the label being correct.",
                                  examples=[0.962, 0.123])


class ImageBinaryClassificationResult(BaseModel):
    prediction: str = Field(...,
                            description="Predicted binary label",
                            examples=["nazi", "non-nazi"])
    confidence: Optional[float] = Field(None,
                                        description="Confidence of the prediction.",
                                        examples=[0.962, 0.123])


class ImageMulticlassClassificationResult(BaseModel):
    nazi_symbols: List[str] = Field(...,
                                    description="List of container nazi symbols",
                                    examples=[["Black Sun",
                                               "Flash and circle",
                                               "Broken Sun Cross",
                                               "The Happy Merchant",
                                               "Hitler",
                                               "Nazi salute",
                                               "Yellow badge",
                                               "neo-Nazi",
                                               "Siegrune",
                                               "SS Skull",
                                               "Sturmabteilung emblem",
                                               "Swastika",
                                               "Wolfsangel"]])
    details: List[ImageClassificationResultDetails] = Field(...)


class ImageClassificationResult(ImageMulticlassClassificationResult):
    """Represents the result of an image classification."""
    containing_nazi_symbols: bool = Field(...,
                                          description="Whether the given image containing nazi symbols.",
                                          examples=[True, False])
    prob: Optional[float] = Field(None,
                                  description="Probability of the label being correct.",
                                  examples=[0.962, 0.123])


class PredictBinaryResponse(BaseModel):
    results: List[ImageBinaryClassificationResult] = Field(...)


class PredictMulticlassResponse(BaseModel):
    results: List[ImageMulticlassClassificationResult] = Field(...)


class PredictResponse(BaseModel):
    results: List[ImageClassificationResult] = Field(...)
