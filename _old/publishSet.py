import maya.cmds as cmds
import os
from modules import publish

def pSet():

	newPath, path = publish.publish()

	#create publish file
	cmds.file(rename=newPath)
	cmds.file(type='mayaBinary', save=True)
	cmds.select(clear=True)
	
	#import reference
	refs = cmds.ls(references=True)
	for ref in refs:
		print(ref)
		refPath = cmds.referenceQuery(ref, filename=True)
		nm = cmds.referenceQuery(ref, namespace=True)

		cmds.file(refPath, importReference=True)
	
	#create __SET__ group
	tops = cmds.ls(assemblies=True)
	grps = []

	for top in tops: 
		shapes = cmds.listRelatives(top, shapes=True)
		if not shapes:
			grps.append(top)
	        
	cmds.select(grps, replace=True)
	cmds.group(grps, n="__SET__")

	#re open working scene
	cmds.file(save=True)
	cmds.file(path, open=True)

	#end
	cmds.select(clear=True)
	cmds.confirmDialog(title="Publish", message="Publish SET Done", button=['Ok'], defaultButton="Ok")
