from dataclasses import dataclass, field


@dataclass
class SanityReport:
    passed_check: list = field(default_factory=list)
    resolved_check: list = field(default_factory=list)
    failed_check: list = field(default_factory=list)
    failed_execution: list = field(default_factory=dict)


class SanityRunner:
    def __init__(self) -> None:
        pass