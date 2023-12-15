from abc import ABC, abstractmethod
from typing import List

from vulcain.python.procedure.shared.procedure import ProcedureContext
from vulcain.python.procedure.shared.process import Process


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
            each.set_has_run(True)

        self.after_execute.extend(context)

        return context

    def revert_processes(self, processes: List[Process], context: ProcedureContext) -> ProcedureContext:
        """"""
        self.before_revert.extend(context)

        for each in processes:
            if each.get_has_run():
                context = each.revert()

        self.after_revert.extend(context)

        return context

