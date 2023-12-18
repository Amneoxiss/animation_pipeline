from abc import ABC, abstractmethod

from vulcain.procedure.shared.procedure import ProcedureContext


class Process(ABC):
    def __init__(self) -> None:
        self._has_run = False

    @abstractmethod
    def check(self, context: ProcedureContext) -> ProcedureContext:
        """Check before executing."""

    @abstractmethod
    def execute(self, context: ProcedureContext) -> ProcedureContext:
        """Execute something to do."""

    @abstractmethod
    def revert(self, context: ProcedureContext) -> ProcedureContext:
        """Revert to do in case of fail execution."""

    def set_has_run(self, value: bool) -> None:
        self._has_run = value

    def get_has_run(self) -> bool:
        return self._has_run

    class CheckFailed(Exception):
        pass