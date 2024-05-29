from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List
from enum import Enum, auto

from vulcain.context import VulcainContext
from vulcain.logger import Logger
from vulcain.procedure.shared.ui.procedure_ui import ProcedureUI
from vulcain.procedure.shared.software import Software, DefaultSoftware
from vulcain.context import VulcainContext


logger = Logger(name="Procedure")


@dataclass
class ProcedureContext:
    context = VulcainContext
    input_args: dict = {}
    any_context: dict = {}
    return_value: Any = None


class ProcedureStatus(Enum):
    CHECK_FAIL = auto()
    EXECUTE_FAIL = auto()
    REVERT_FAIL = auto()
    SUCCESS = auto()


class Procedure(ABC):
    def __init__(self, context: VulcainContext, ui: ProcedureUI = None, dcc: Software = None) -> None:
        self.context = context
        self.ui = ui
        self.dcc = dcc or DefaultSoftware()
        self.wrong_checks: list = []
        self.status: ProcedureStatus = ProcedureStatus.SUCCESS

    class CheckFailed(Exception):
        def __init__(self, message, wrong_checks: list) -> None:
            super().__init__(message)
            self.wrong_checks = wrong_checks

    def launch(self) -> Any:
    
        if self.dcc:
            self.dcc.start()

        try:
            self.context = self.check()
        except self.CheckFailed as err:
            self.wrong_checks = err.wrong_checks
            self.status = ProcedureStatus.CHECK_FAIL
        except Exception:
            logger.exception("Exception occured while checking before execution.")
            self.status = ProcedureStatus.CHECK_FAIL

        if self.status != ProcedureStatus.CHECK_FAIL:
            try:
                self.execute()
            except Exception:
                logger.exception("Exception occured while executing the procedure.")
                self.status = ProcedureStatus.EXECUTE_FAIL

        if self.status == ProcedureStatus.CHECK_FAIL or self.status == ProcedureStatus.EXECUTE_FAIL:
            try:
                self.revert()
            except Exception:
                logger.exception("Exception occured while reverting the procedure.")
                self.status = ProcedureStatus.REVERT_FAIL

        self.end_launch()

        if self.dcc:
            self.dcc.stop()

        return self.context.return_value

    @abstractmethod
    def pre_check(self):
        """"""

    @abstractmethod
    def post_check(self):
        """"""

    @abstractmethod
    def check(self):
        """"""

    @abstractmethod
    def pre_execute(self):
        """"""

    @abstractmethod
    def post_execute(self):
        """"""

    @abstractmethod
    def execute(self):
        """"""

    @abstractmethod
    def pre_revert(self):
        """"""

    @abstractmethod
    def post_revert(self):
        """"""

    @abstractmethod
    def revert(self):
        """"""

    def end_launch(self):
        if self.status == ProcedureStatus.CHECK_FAIL and self.status != ProcedureStatus.REVERT_FAIL:
            wrong_checks = "\n- ".join(self.wrong_checks)
            message = f"Some checks are wrong. Execution can't start.\n{wrong_checks}"
            self.ui.show_end_fail_message(self.context.name, message)

        elif self.status == ProcedureStatus.CHECK_FAIL and self.status == ProcedureStatus.REVERT_FAIL:
            message = f"Revert procedure failed after a check fail."
            self.ui.show_end_fail_message(self.context.name)

        elif self.status == ProcedureStatus.EXECUTE_FAIL and self.status != ProcedureStatus.REVERT_FAIL:
            message = f"Execution has failed."
            self.ui.show_end_fail_message(self.context.name)

        elif self.status == ProcedureStatus.EXECUTE_FAIL and self.status == ProcedureStatus.REVERT_FAIL:
            message = f"Revert procedure failed after an execution fail."
            self.ui.show_end_fail_message(self.context.name, message)

        else:
            self.ui.show_end_success_message(self.context.name)


if __name__ == "__main__":
    procedure = Procedure()
    procedure.launch()