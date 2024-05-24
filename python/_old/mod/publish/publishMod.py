import maya.cmds as cmds
from maya.mel import eval
import os
import sys
sys.path.append("../..")
from modules import publish

def checkPublish():
	
	cmds.select("MOD_grp", replace=True, hierarchy=True)
	objs = cmds.ls(selection=True, exactType="transform") 
	cmds.select(objs, replace=True)
	grps=[]
	geos=[]

	for obj in objs:
		shape = cmds.listRelatives(obj, shapes=True)
		if not shape :
			print(obj + " is a transform")
			grps.append(obj)
		else :
			nType = cmds.nodeType(shape)

			if nType != "mesh":
				print(obj + " is " + nType)
				cmds.confirmDialog(title="Warning", message="Unexpected shapes in MOD_grp !",button=['Cancel'], defaultButton="Cancel")
				break
			else:
				print(obj + " is a mesh")
				geos.append(obj)
	print(grps)
	print(geos)

	for grp in grps:
		if grp.__contains__("_grp"):
			if grp.__contains__("c_") or grp.__contains__("l_") or grp.__contains__("r_") or grp.__contains__("MOD_"):
				print(grp + " : is a good name")
		else :
			print(grp + " : is not a good name")
			cmds.confirmDialog(title="Warning", message="Nomenclature !",button=['Cancel'], defaultButton="Cancel")
			break

	for geo in geos:
		if geo.__contains__("_geo"):
			if geo.__contains__("c_") or geo.__contains__("l_") or geo.__contains__("r_"):
				print(geo + " : is a good name")
		else :
			print(geo + " : is not a good name")
			cmds.confirmDialog(title="Warning", message="Nomenclature !",button=['Cancel'], defaultButton="Cancel")
			break
	print("Publish Done")
	
def pMod():

	#init value
	ext = "abc"
	pubFolder = "_Publish"

	#get selection
	cmds.select("MOD_grp", replace=True)
	mod = cmds.ls(selection=True)
	
	#publish script
	newPath, path = publish.publish(ext, pubFolder)

	#publish mod to abc and end of script
	eval('AbcExport -j "-root {0} -file {1} -uv -ws -wuvs "'.format(mod[0], newPath))
	cmds.confirmDialog(title="Publish", message="Publish MOD Done", button=['Ok'], defaultButton="Ok")
	cmds.select(clear=True)