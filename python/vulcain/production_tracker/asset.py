from enum import Enum, auto


class AssetType(Enum):
    ACTORS = auto()
    PROPS = auto()
    SET = auto()


class AssetCategory(Enum):
    HUMAIN = "humn"
    ANIMAL = "anml"
    FURNITURE = "furn"
    FOLIAGE = "folg"
    ENVIRONMENT = "evnm"


class AssetOrigin(Enum):
    FULL = auto()
    VARIATION = auto()
    DERIVATED = auto()
