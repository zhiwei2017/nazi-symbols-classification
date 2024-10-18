from enum import Enum


class FlipDirection(Enum):
    VERTICALLY = 0
    HORIZONTALLY = 1


class EnumExtend:
    _member_names_ = []
    _value2member_map_ = dict()

    @classmethod
    def names(cls):
        return cls._member_names_

    @classmethod
    def values(cls):
        return list(cls._value2member_map_.keys())


class NonZeroSign(int, EnumExtend, Enum):
    POS = 1
    NEG = -1


class ZeroSign(int, EnumExtend, Enum):
    ZERO = 0
    POS = 1
    NEG = -1
