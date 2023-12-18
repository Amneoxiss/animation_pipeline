from vulcain.procedure.shared import Process
from vulcain.procedure.shared.procedure import ProcedureContext


class InitScene(Process):
    def check(self, context: ProcedureContext) -> ProcedureContext:
        pass

    def execute(self, context: ProcedureContext) -> ProcedureContext:
        pass 

    def revert(self, context: ProcedureContext) -> ProcedureContext:
        pass
