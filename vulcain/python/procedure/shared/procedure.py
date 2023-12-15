import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List


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
    def extend(self, context: ProcedureContext) -> ProcedureContext:
        """"""


class DefaultExpander(Expander):
    def extend(self, context: ProcedureContext) -> ProcedureContext:
        return context


class Executor(ABC):
    @abstractmethod
    def check_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def execute_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def revert_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""


class ProcessExecutor(Executor):
    def __init__(self,
                 before_check: Expander = None,
                 after_check: Expander = None,
                 before_execute: Expander = None,
                 after_execute: Expander = None,
                 before_revert: Expander = None,
                 after_revert: Expander = None) -> None:

        self.before_check = before_check or DefaultExpander()
        self.after_check = after_check or DefaultExpander()
        self.before_execute = before_execute or DefaultExpander()
        self.after_execute = after_execute or DefaultExpander()
        self.before_revert = before_revert or DefaultExpander()
        self.after_revert = after_revert or DefaultExpander()

    def check_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""
        self.before_check.extend(context)

        for each in processes:
            context = each.check(context)

        self.after_check.extend(context)

        return context

    def execute_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""
        self.before_execute.extend(context)
        
        for each in processes:
            context = each.execute(context)
            each.set_run_status(True)

        self.after_execute.extend(context)

        return context

    def revert_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""
        self.before_revert.extend(context)

        for each in processes:
            if each.get_run_status():
                context = each.revert()

        self.after_revert.extend(context)

        return context


class Procedure():
    def __init__(self, processes: List[Process], context: ProcedureContext, executor: Executor, ui: ProcedureUI = None, dcc: DCC = None):
        self.processes = processes
        self.context = context
        self.ui = ui
        self.executor = executor
        self.dcc = dcc
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
            self.dcc.stop_dcc()

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