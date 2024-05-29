from dataclasses import dataclass, field


@dataclass
class VulcainContext:
    section: str
    episode: str = ""
    sequence: str =""
    shot: str = ""
    asset: str = ""
    step: str = ""
    task: str = ""
    version: int = field(default_factory=None)
    software: str = ""
    extra: str = ""
    labels: list = field(default_factory=list)   
