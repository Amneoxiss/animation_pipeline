import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any 


from vulcain.python.procedure.shared.vulcain_arg import VArg
from vulcain.python.pipeline_exceptions import ArgumentMissing
from vulcain.python.logger import Logger

logger = Logger(name="Maya Procedure")


@dataclass
class ProcedureContext:
    varg: VArg
    path_maker_context: dict = {}
    return_value: Any = None
    any_context: dict = {}


class Process(ABC):
    def __init__(self) -> None:
        self.failed_check: list = []

    @abstractmethod
    def check(context: ProcedureContext) -> ProcedureContext:
        """Check before executing."""

    @abstractmethod
    def execute(context: ProcedureContext) -> ProcedureContext:
        """Execute something to do."""

    @abstractmethod
    def revert(context: ProcedureContext) -> ProcedureContext:
        """Revert to do in case of fail execution."""

    class CheckFailed(Exception):
        pass


class DCC(ABC):
    @abstractmethod
    def start_dcc():
        pass

    @abstractmethod
    def stop_dcc():
        pass


class Expander(ABC):
    @abstractmethod
    def before_check(context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def after_check(context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def before_execute(context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def after_execute(context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def before_revert(context: ProcedureContext) -> ProcedureContext:
        """"""

    @abstractmethod
    def after_revert(context: ProcedureContext) -> ProcedureContext:
        """"""


class Procedure():
    def __init__(self, processes: list(Process), context: ProcedureContext, expander: Expander = None, dcc: DCC = None):
        self.processes = processes
        self.context = context
        self.expander = expander
        self.dcc = dcc

    def execute(self, processes: list(Process), expander: Expander = None):

        if self.dcc:
            self.dcc.start_dcc()

        # CHECK PROCEDURE
        check_before_procedure_fail = False
        try:
            self.context= self.check_processes(processes)
        except Exception as err:
            traceback.print_exc()
            logger.error(err)
            check_before_procedure_fail = True

        if check_before_procedure_fail:
            try:
                self.revert_check_procedure()
                self.end_execute(check_fail=True, check_revert_fail=False)
            except Exception as err:
                self.end_execute(check_fail=True, check_revert_fail=True)

            return

        # PROCEDURE
        procedure_fail = False
        try:
            self.procedure()
        except Exception as err:
            traceback.print_exc()
            logger.error(err)
            procedure_fail = True

        if procedure_fail:
            try:
                self.revert_procedure()
                self.end_execute(fail=True, revert_fail=False)
            except Exception as err:
                self.end_execute(fail=True, revert_fail=True)
        else:
            self.end_execute()

        if self.dcc:
            self.dcc.stop_dcc()

    def check_processes(self, processes: list(Process), context: ProcedureContext) -> ProcedureContext:
        """"""
        if self.expander:
            context = self.expander.before_check(context)

        for each in processes:
            context = each.check()

        if self.expander:
            context = self.expander.after_check(context)

        return context
    
    def execute_processes(self, processes: list(Process), context: ProcedureContext) -> ProcedureContext:
        """"""
        if self.expander:
            context = self.expander.before_execute(context)
        
        for each in processes:
            context = each.execute(context)

        if self.expander:
            context = self.expander.after_execute(context)

        return context

    def revert_processes(self, processes: list(Process), context: ProcedureContext) -> ProcedureContext:
        """"""
        if self.expander:
            context = self.expander.before_revert(context)

        for each in processes:
            context = each.revert()

        if self.expander:
            context = self.expander.after_revert(context)

        return context


if __name__ == "__main__":
    procedure = Procedure()
    procedure.execute()