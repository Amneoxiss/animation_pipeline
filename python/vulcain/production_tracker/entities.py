from abc import ABC
from dataclasses import dataclass

from .statuses import AssetStatus, ShowStatus, SequenceStatus, ShotStatus, \
    TaskArtStatus, TaskPipelineStatus, VersionLeadStatus, VersionSupStatus, \
    VersionRealStatus, VersionClientStatus, VersionPipelineStatus

from .asset import AssetType, AssetOrigin, AssetCategory


@dataclass
class Entity(ABC):
    name: str
    id: int
    description: str = ""


@dataclass
class Asset(Entity):
    status: AssetStatus
    type: AssetType
    origin: AssetOrigin
    category: AssetCategory


@dataclass
class Show(Entity):
    status: ShowStatus


@dataclass
class Sequence(Entity):
    status: SequenceStatus


@dataclass
class Shot(Entity):
    status: ShotStatus


@dataclass
class Task(Entity):
    art_status: TaskArtStatus
    pipeline_status: TaskPipelineStatus
    pipeline_report: str = ""
    asset_id: int = None
    show_id: int = None
    sequence_id: int = None
    shot_id: int = None


@dataclass
class Version(Entity):
    task_id_link: int
    lead_status: VersionLeadStatus
    sup_status: VersionSupStatus
    real_status: VersionRealStatus
    client_status: VersionClientStatus
    pipeline_status: VersionPipelineStatus
    pipeline_report: str = ""
