import maya.cmds as cmds
import os
import sys
sys.path.append("../..")
from modules import publish

	
def pLdev():

	#init value
	ext ="mb"
	pubFolder = "_Publish"

	sel = cmds.ls(selection=True)
	print(sel)

	if not sel:
		cmds.error("Please select something")

	else:
		newPath, path = publish.publish()

		print(newPath, path)

		if not os.path.exists(newPath):
			os.makedirs(newPath)
		
		cmds.file(newPath, type='mayaBinary', exportSelected=True)
		cmds.confirmDialog(title="Publish", message="Publish Lookdev Done", button=['Ok'], defaultButton="Ok")
		cmds.select(clear=True)