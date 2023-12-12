import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List 


from vulcain.python.procedure.shared.vulcain_arg import VArg
from vulcain.python.pipeline_exceptions import ArgumentMissing
from vulcain.python.logger import Logger

logger = Logger(name="Maya Procedure")


@dataclass
class ProcedureContext:
    varg: VArg
    path_maker_context: dict = {}
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


class Procedure(ABC):
    def __init__(self, context):
        self.execution_from_ddc = True  # TODO: Find a way to known if were in a shell or in a dcc
        self.context: ProcedureContext = context

    def execute(self, processes: list(Process)):

        self.init_software()

        # CHECK PROCEDURE
        check_before_procedure_fail = False
        try:
            self.check_before_procedure()
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

    @abstractmethod
    def init_software(self):
        """Method to start a software."""

    @abstractmethod
    def stop_sofware():
        """Stop the software after the execution."""

    @abstractmethod
    def _execute_processes():
        """"""
    
    @abstractmethod
    def _check_processes():
        """"""

if __name__ == "__main__":
    procedure = MayaProcedure()
    procedure.execute()