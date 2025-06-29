"""Module for defining constants centrally."""
from enum import Enum


class ModelType(str, Enum):
    """Enumeration for model types used in the classification backend."""
    SVC = "SVC"
    YOLO = "YOLO"
