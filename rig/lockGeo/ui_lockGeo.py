from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import lockGeo

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class LockGeoDialog(QtWidgets.QDialog):

	qmw_instance = None

	@classmethod
	def show_ui(cls):
		if not cls.qmw_instance:
			cls.qmw_instance = LockGeoDialog()

		if cls.qmw_instance.isHidden():
			cls.qmw_instance.show()
		else:
			cls.qmw_instance.raise_()
			cls.qmw_instance.activateWindow()

	def __init__(self, parent=maya_main_window()):
		super(LockGeoDialog, self).__init__(parent)

		self.setWindowTitle("Lock Geo")
		self.setFixedSize(200, 150)
		self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.create_widgets()
		self.create_layout()
		self.create_connection()
    
	def create_widgets(self):
		self.lockAllBtn = QtWidgets.QPushButton("Lock All")
		self.unlockAllBtn = QtWidgets.QPushButton("Unlock All")
		self.lockSelBtn = QtWidgets.QPushButton("Lock Selection")
		self.unlockSelBtn = QtWidgets.QPushButton("Unlock Selection")

	def create_layout(self):
		main_layout = QtWidgets.QVBoxLayout(self)
		main_layout.addWidget(self.lockAllBtn)
		main_layout.addWidget(self.unlockAllBtn)
		main_layout.addWidget(self.lockSelBtn)
		main_layout.addWidget(self.unlockSelBtn)

	def create_connection(self):
		self.lockAllBtn.clicked.connect(self.runLockAll)
		self.unlockAllBtn.clicked.connect(self.runUnlockAll)
		self.lockSelBtn.clicked.connect(self.runLockSel)
		self.unlockSelBtn.clicked.connect(self.runUnlockSel)

	def runLockAll(self):
		lockGeo.lockAll()

	def runUnlockAll(self):
		lockGeo.unlockAll()
	
	def runLockSel(self):
		lockGeo.lockSelected()

	def runUnlockSel(self):
		lockGeo.unlockSelected()

if __name__ == "__main__":

	try:
		lock_geo_dialog.close() # pylint: disable=E0601
		lock_geo_dialog.deleteLater()
	except:
		pass

	lock_geo_dialog = LockGeoDialog()
	lock_geo_dialog.show()