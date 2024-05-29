import maya.cmds as cmds

from ....maya import create_groups_from_dict
from ..procedure import MayaProcedure
from ...shared import ProcedureContext


MODELING_DAG = {
    "root": "ALL",
    "ALL": "GEO",
    "ALL": "GABARIT",
    "root": "TRASH"
}


class BuildModelbase(MayaProcedure):
    def __init__(self, context: ProcedureContext) -> None:
        super().__init__(context)

    def execute(self):
        cmds.file(new=True, force=True)
        create_groups_from_dict(MODELING_DAG)

    def revert(self):
        pass
