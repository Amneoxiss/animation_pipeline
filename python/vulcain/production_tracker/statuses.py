from enum import Enum
from dataclasses import dataclass


class AssetStatus(Enum):
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    COMPLETE = "cmpt"


class ShowStatus(Enum):
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    COMPLETE = "cmpt"


class SequenceStatus(Enum):
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    COMPLETE = "cmpt"


class ShotStatus(Enum):
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    COMPLETE = "cmpt"


class TaskArtStatus(Enum):
    pass


class TaskPipelineStatus(Enum):
    pass


class VersionLeadStatus(Enum):
    pass


class VersionSupStatus(Enum):
    pass


class VersionRealStatus(Enum):
    pass


class VersionClientStatus(Enum):
    pass


class VersionPipelineStatus(Enum):
    pass
