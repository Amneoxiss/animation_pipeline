from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List

from vulcain.procedure.shared.vulcain_path import VulcainPath
from vulcain.logger import Logger
from vulcain.procedure.shared.ui.procedure_ui import ProcedureUI
from vulcain.procedure.shared.software import Software, DefaultSoftware
from vulcain.procedure.shared.process import Process
from vulcain.procedure.shared.executor import Executor

logger = Logger(name="Procedure")


@dataclass
class ProcedureContext:
    varg: VulcainPath
    name: str
    path_maker_context: dict = {}
    input_args: dict = {}
    any_context: dict = {}
    return_value: Any = None


class Procedure(ABC):
    def __init__(self, context: ProcedureContext, ui: ProcedureUI = None, dcc: Software = None):
        self.context = context
        self.ui = ui
        self.dcc = dcc or DefaultSoftware()
        self.wrong_checks: str = ""
        self.check_fail: bool = False
        self.execute_fail: bool = False
        self.revert_fail: bool = False

    class CheckFailed(Exception):
        def __init__(self, message, wrong_checks) -> None:
            super().__init__(message)
            self.wrong_checks = wrong_checks

    def launch(self):
        if self.dcc:
            self.dcc.start_dcc()

        try:
            self.context= self.check_before_executing()
        except self.CheckFailed as err:
            self.wrong_checks = err.wrong_checks
            self.check_fail = True
        except Exception:
            logger.exception("Exception occured while checking before execution.")
            self.check_fail = True

        if not self.check_fail:
            try:
                self.executing()
            except Exception:
                logger.exception("Exception occured while executing the procedure.")
                self.execute_fail = True

        if self.execute_fail or self.check_fail:
            try:
                self.revert_after_execute()
            except Exception:
                logger.exception("Exception occured while reverting the procedure.")
                self.revert_fail = True

        if self.dcc:
            self.dcc.stop_dcc()

        self.end_launch()

        return self.context.return_value

    @abstractmethod
    def check_before_executing(self):
        """"""

    @abstractmethod
    def executing(self):
        """"""

    @abstractmethod
    def revert_after_execute(self):
        """"""

    def end_launch(self):
        if self.check_fail and not self.revert_fail:
            wrong_checks = "\n- ".join(self.wrong_check)
            message = f"Some checks are wrong. Execution can't start.\n{wrong_checks}"
            self.ui.show_end_fail_message(self.context.name, message)

        elif self.check_fail and self.revert_fail:
            message = f"Revert procedure failed after a check fail."
            self.ui.show_end_fail_message(self.context.name)

        elif self.execute_fail and not self.revert_fail:
            message = f"Execution has failed."
            self.ui.show_end_fail_message(self.context.name)

        elif self.execute_fail and self.revert_fail:
            message = f"Revert procedure failed after an execution fail."
            self.ui.show_end_fail_message(self.context.name, message)

        else:
            self.ui.show_end_success_message(self.context.name)


class HardProcedure():
    def __init__(self, processes: List[Process], context: ProcedureContext, executor: Executor, ui: ProcedureUI = None, dcc: Software = None):
        self.processes = processes
        self.context = context
        self.ui = ui
        self.executor = executor
        self.dcc = dcc or DefaultSoftware()
        self.wrong_check: str = ""
        self.check_fail: bool = False
        self.execute_fail: bool = False
        self.revert_fail: bool = False

    def launch(self):
        if self.dcc:
            self.dcc.start_dcc()

        try:
            self.context= self.executor.check_processes(self.processes, self.context)
        except Process.CheckFailed as wrong_check:
            self.wrong_check = wrong_check
            self.check_fail = True
        except Exception:
            logger.exception("Exception occured while checking before execution.")
            self.check_fail = True

        if not self.check_fail:
            try:
                self.executor.execute_processes(self.processes, self.context)
            except Exception:
                logger.exception("Exception occured while executing the procedure.")
                self.execute_fail = True

        if self.execute_fail or self.check_fail:
            try:
                self.executor.revert_processes(self.processes, self.context)
            except Exception:
                logger.exception("Exception occured while reverting the procedure.")
                self.revert_fail = True

        if self.dcc:
            self.dcc.stop()

        self.end_launch()

        return self.context.return_value

    def end_launch(self):
        if self.check_fail and not self.revert_fail:
            wrong_checks = "\n- ".join(self.wrong_check)
            message = f"Some checks are wrong. Execution can't start.\n{wrong_checks}"
            self.ui.show_end_fail_message(self.context.name, message)

        elif self.check_fail and self.revert_fail:
            message = f"Revert procedure failed after a check fail."
            self.ui.show_end_fail_message(self.context.name)

        elif self.execute_fail and not self.revert_fail:
            message = f"Execution has failed."
            self.ui.show_end_fail_message(self.context.name)

        elif self.execute_fail and self.revert_fail:
            message = f"Revert procedure failed after an execution fail."
            self.ui.show_end_fail_message(self.context.name, message)

        else:
            self.ui.show_end_success_message(self.context.name)


if __name__ == "__main__":
    procedure = Procedure()
    procedure.launch()