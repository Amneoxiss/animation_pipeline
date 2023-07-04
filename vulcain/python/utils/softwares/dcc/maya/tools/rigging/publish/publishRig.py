import maya.cmds as cmds
import os
import sys
sys.path.append("../..")
from modules import publish


def pRig() :

	#init value
	ext ="mb"
	pubFolder = "_Publish"
	
	#Save Scene
	cmds.file(save=True)

	#Publish Script
	newPath, path = publish.publish(ext, pubFolder)

	#Save as to publish
	cmds.file(rename=newPath)
	cmds.file(type='mayaBinary', save=True)
	cmds.select(clear=True)

	#import reference
	cmds.select("*RN")
	ref = cmds.ls(selection=True)
	refPath = cmds.referenceQuery(ref[0], filename=True)
	nm = cmds.referenceQuery(ref[0], namespace=True)

	cmds.file(refPath, importReference=True)

	#delete namespace	
	cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=nm)
	

	#re open working scene
	cmds.file(save=True)
	
	cmds.confirmDialog(title="Publish", message="Publish RIG Done", button=['Ok'], defaultButton="Ok")