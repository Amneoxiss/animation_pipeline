from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as om

def lockSelected():

	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 1)
		cmds.setAttr(geo+".overrideDisplayType", 2)

def unlockSelected():

	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 0)
		cmds.setAttr(geo+".overrideDisplayType", 0)

def lockAll():

	cmds.select("*:*_geo", replace=True)
	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 1)
		cmds.setAttr(geo+".overrideDisplayType", 2)

	cmds.select(clear=True)

def unlockAll():

	cmds.select("*:*_geo", replace=True)
	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 0)
		cmds.setAttr(geo+".overrideDisplayType", 0)

	cmds.select(clear=True)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class LockGeoDialog(QtWidgets.QDialog):

    def __inti__(self, parent=maya_main_window()):
        super(LockGeoDialog, self).__init__(parent)

        self.setWindowTitle("Lock Geo")
        self.setMinimumSize(400, 100)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connection()
    
    def create_widgets():
        pass

    def create_layout():
        pass

    def create_connection():
        pass