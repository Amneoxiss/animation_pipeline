import maya.cmds as cmds

from vulcain.python.procedure.softwares.dcc.maya.procedure import MayaProcedure

class Build(MayaProcedure):
    def __init__(self):
        super().__init__()
    
    def procedure(self, task_path, **kwargs):
        cmds.delete("TRASH")
        
        if cmds.listRelatives("CTN"):
            raise NotImplementedError("CTN export is not implemented for the moment.")
        
        cmds.delete("CTN")
        cmds.ls("MDB", long=True)

        # Export Alembic.
        # Export GpuCache.