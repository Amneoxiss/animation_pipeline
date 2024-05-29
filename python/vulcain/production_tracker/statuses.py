from enum import Enum
from dataclasses import dataclass


class AssetStatus(Enum):
    OMIT = "omt"
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    ON_HOLD = "ohd"
    COMPLETE = "cmpt"


class ShowStatus(Enum):
    OMIT = "omt"
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    ON_HOLD = "ohd"
    COMPLETE = "cmpt"


class SequenceStatus(Enum):
    OMIT = "omt"
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    ON_HOLD = "ohd"
    COMPLETE = "cmpt"


class ShotStatus(Enum):
    OMIT = "omt"
    WAITING = "wtg"
    IN_PROGRESS = "ip"
    ON_HOLD = "ohd"
    COMPLETE = "cmpt"


class TaskArtStatus(Enum):
    OMIT = "omt"
    WAITING = "wtg"
    ON_HOLD = "ohd"
    BUILD_OK = "bldok"
    BUILD_ERROR = "blderr"
    IN_PROGRESS = "ip"
    SNAP_ERROR = "snperr"
    PENDING_REVIEW_LEAD = "pdrled"
    PENDING_REVIEW_SUP = "pdrsup"
    PENDING_REVIEW_REAL = "pdrrel"
    PENDING_REVIEW_CLIENT = "pdrclt"
    PENDING_REVIEW_PROD = "pdrpod"
    RETAKE_REVIEW_LEAD = "rtkld"
    RETAKE_REVIEW_SUP = "rtksup"
    RETAKE_REVIEW_REAL = "rtkrel"
    RETAKE_REVIEW_CLIENT = "rtkclt"
    RETAKE_REVIEW_PROD = "rtkprod"
    RETAKE_TECH = "rtktc"
    READY_TO_PUBLISH = "rdypub"
    COMPLETE = "cmpt"
    TEMPORARY = "tmp"


class VersionLeadStatus(Enum):
    NOT_APPLICABLE = "na"
    PENDING_REVIEW = "pdr"
    RETAKE = "rtk"
    OK = "ok"
    COMPLETE = "cmp"


class VersionSupStatus(Enum):
    NOT_APPLICABLE = "na"
    PENDING_REVIEW = "pdr"
    RETAKE = "rtk"
    OK = "ok"
    COMPLETE = "cmp"


class VersionRealStatus(Enum):
    NOT_APPLICABLE = "na"
    PENDING_REVIEW = "pdr"
    RETAKE = "rtk"
    OK = "ok"
    COMPLETE = "cmp"


class VersionClientStatus(Enum):
    NOT_APPLICABLE = "na"
    PENDING_REVIEW = "pdr"
    RETAKE = "rtk"
    OK = "ok"
    COMPLETE = "cmp"


class VersionProdStatus(Enum):
    NOT_APPLICABLE = "na"
    PENDING_REVIEW = "pdr"
    RETAKE = "rtk"
    OK = "ok"
    COMPLETE = "cmp"


class VersionPipelineStatus(Enum):
    SANITY_ERROR = "snterr"
    OK = "ok"
    RETAKE = "rtk"
    PUBLISH_ERROR = "puberr"
    COMPLETE = "cmp"
    TEMPORARY = "tmp"
