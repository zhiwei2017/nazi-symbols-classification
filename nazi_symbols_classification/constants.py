from enum import Enum


class FlipDirection(Enum):
    VERTICALLY = 0
    HORIZONTALLY = 1


class NonZeroSign(int, Enum):
    POS = 1
    NEG = -1

    @classmethod
    def name(cls):
        return cls._member_names_

    @classmethod
    def values(cls):
        return list(cls._value2member_map_.keys())


class ZeroSign(NonZeroSign):
    ZERO = 0
