from enum import Enum
from typing import List, Dict, Any


class FlipDirection(Enum):
    VERTICALLY = 0
    HORIZONTALLY = 1


class EnumExtend:
    _member_names_: List[str] = []
    _value2member_map_: Dict[str, Any] = dict()

    @classmethod
    def names(cls) -> List[str]:
        return cls._member_names_

    @classmethod
    def values(cls) -> List[Any]:
        return list(cls._value2member_map_.keys())


class NonZeroSign(int, EnumExtend, Enum):
    POS = 1
    NEG = -1


class ZeroSign(int, EnumExtend, Enum):
    ZERO = 0
    POS = 1
    NEG = -1
