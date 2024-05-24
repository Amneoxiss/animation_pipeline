import maya.standalone

from vulcain.procedure.shared.software import Software


class Maya(Software):
    def start(self):
        maya.standalone.initialize()

    def stop(self):
        maya.standalone.unitialize()