import maya.cmds as cmds

from vulcain.python.utils.params import param
from vulcain.python.procedure.softwares.dcc.maya.procedure import MayaProcedure
import vulcain.python.utils.softwares.dcc.maya.modules.shared.shared as maya_utils

class Build(MayaProcedure):
    def __init__(self):
        super().__init__()
    
    def procedure(self, task_path, **kwargs):
        maya_utils.create_groups_from_dict(param("modelbase_base_group"))