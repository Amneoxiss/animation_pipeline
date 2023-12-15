import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any 


from vulcain.python.procedure.shared.vulcain_arg import VArg
from vulcain.python.pipeline_exceptions import ArgumentMissing
from vulcain.python.logger import Logger
from vulcain.python.procedure.shared.ui.procedure_ui import ProcedureUI

logger = Logger(name="Maya Procedure")


@dataclass
class ProcedureContext:
    varg: VArg
    name: str
    path_maker_context: dict = {}
    input_args: dict = {}
    any_context: dict = {}
    return_value: Any = None


class Process(ABC):
    def __init__(self) -> None:
        self._failed_checks: list = []
        self._run_status = False

    @abstractmethod
    def check(self, context: ProcedureContext) -> ProcedureContext:
        """Check before executing."""

    @abstractmethod
    def execute(self, context: ProcedureContext) -> ProcedureContext:
        """Execute something to do."""

    @abstractmethod
    def revert(self, context: ProcedureContext) -> ProcedureContext:
        """Revert to do in case of fail execution."""

    def set_run_status(self, status: bool) -> None:
        self._run_status = status

    def get_run_status(self) -> bool:
        return self._run_status

    class CheckFailed(Exception):
        pass


class DCC(ABC):
    @abstractmethod
    def start_dcc(self):
        pass

    @abstractmethod
    def stop_dcc(self):
        pass


class Expander(ABC):
    @abstractmethod
    def before_check(self, context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def after_check(self, context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def before_execute(self, context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def after_execute(self, context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def before_revert(self, context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def after_revert(self, context: ProcedureContext) -> ProcedureContext:
        """"""

# TODO: Create an ProcessIterator to take care of the check, execute and revert method of the Procedure.

class Procedure():
    def __init__(self, processes: list(Process), context: ProcedureContext, ui: ProcedureUI = None, expander: Expander = None, dcc: DCC = None):
        self.processes = processes
        self.context = context
        self.ui = ui
        self.expander = expander
        self.dcc = dcc
        self.wrong_check: str = ""
        self.check_fail: bool = False
        self.execute_fail: bool = False
        self.revert_fail: bool = False

    def launch(self):
        if self.dcc:
            self.dcc.start_dcc()

        try:
            self.context= self.check_processes(self.processes)
        except Process.CheckFailed as wrong_check:
            self.wrong_check = wrong_check
            self.check_fail = True
        except Exception:
            logger.exception("Exception occured while checking before execution.")
            self.check_fail = True

        if not self.check_fail:
            try:
                self.execute_processes(self.processes)
            except Exception:
                logger.exception("Exception occured while executing the procedure.")
                self.execute_fail = True

        if self.execute_fail or self.check_fail:
            try:
                self.revert_processes(self.processes)
            except Exception:
                logger.exception("Exception occured while reverting the procedure.")
                self.revert_fail = True

        if self.dcc:
            self.dcc.stop_dcc()

        self.end_launch()

        return self.context.return_value

    def check_processes(self) -> ProcedureContext:
        """"""
        if self.expander:
            self.context = self.expander.before_check(self.context)

        for each in self.processes:
            self.context = each.check(self.context)

        if self.expander:
            self.context = self.expander.after_check(self.context)

        return self.context

    def execute_processes(self) -> ProcedureContext:
        """"""
        if self.expander:
            self.context = self.expander.before_execute(self.context)
        
        for each in self.processes:
            self.context = each.execute(self.context)
            each.set_run_status(True)

        if self.expander:
            self.context = self.expander.after_execute(self.context)

        return self.context

    def revert_processes(self, processes: list(Process), context: ProcedureContext) -> ProcedureContext:
        """"""
        if self.expander:
            context = self.expander.before_revert(context)

        for each in processes:
            if each.get_run_status() :
                context = each.revert()

        if self.expander:
            context = self.expander.after_revert(context)

        return context

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
