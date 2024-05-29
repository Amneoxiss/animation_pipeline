from ..shared import Procedure, ProcedureContext, ProcedureUI, Software


class MayaProcedure(Procedure):
    def __init__(self, context: ProcedureContext, ui: ProcedureUI = None, dcc: Software = None) -> None:
        super().__init__(context, ui, dcc)

    def pre_check(self):
        pass

    def check(self):
        pass

    def post_check(self):
        pass

    def pre_execute(self):
        pass
    
    def execute(self):
        pass

    def post_execute(self):
        pass

    def pre_revert(self):
        pass

    def revert(self):
        pass

    def post_revert(self):
        pass
