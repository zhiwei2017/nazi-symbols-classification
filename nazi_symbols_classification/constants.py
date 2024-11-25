from enum import Enum
from typing import List, Dict, Any


class FlipDirection(Enum):
    """Enumeration class for flip directions: horizontally and vertically."""
    VERTICALLY = 0
    HORIZONTALLY = 1


class EnumExtend:
    """Extended enumeration class with function `names` for returning names of
    enum items and function `values` for returning values of enum item"""
    _member_names_: List[str] = []
    _value2member_map_: Dict[str, Any] = dict()

    @classmethod
    def names(cls) -> List[str]:
        return cls._member_names_

    @classmethod
    def values(cls) -> List[Any]:
        return list(cls._value2member_map_.keys())


class NonZeroSign(int, EnumExtend, Enum):
    """Non zero sign enumeration class with item pos for 1 and neg for -1."""
    POS = 1
    NEG = -1


class ZeroSign(int, EnumExtend, Enum):
    """Zero sign enumeration class with item pos for 1, neg for -1 and zero
    for 0."""
    ZERO = 0
    POS = 1
    NEG = -1
