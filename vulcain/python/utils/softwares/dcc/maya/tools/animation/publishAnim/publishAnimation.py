import maya.cmds as cmds
from maya.mel import eval
import json
import os


def publish():

	cmds.select("*:MOD_grp", replace=True)
	mods = cmds.ls(selection=True)
	path = cmds.file(query=True, sceneName=True)
	directory, filename = os.path.split(path)

	directory = os.path.join(directory, "_Publish")

	#Frame range
	fIn = cmds.playbackOptions(q=True, animationStartTime=True)
	fOut = cmds.playbackOptions(q=True, animationEndTime=True)
	fps = cmds.currentUnit(query=True, time=True)

	#Create dictionnary for animation info
	fRange = dict()

	fRange["In"] = fIn
	fRange["Out"] = fOut
	fRange["fps"] = fps

	#Create json file for animation info
	jsonName = filename.split("_")[0]
	jsonName = jsonName.replace("ANIM", "")
	jsonPath = os.path.join(directory, "{}.json".format(jsonName)).replace("\\", "/")

	
	with open(jsonPath, 'w') as f:
		json.dump(fRange, f)
	
	
	#create folder each object
	for mod in mods:
		namespace = mod.rpartition(':')[0]
		name = filename.replace("ANIM.ma", '_'+namespace)

		folder = os.path.join(directory, "Alembic", namespace).replace("\\","/")

		if os.path.exists(folder):
			pass

		else :
			os.makedirs(folder)


		#Select mod for each object and export abc
		cmds.select(mod, replace=True)
		eval('AbcExport -j "-fr {0} {1} -root {2} -file {3}/{4}.abc -uv -ws -wuvs "'.format(fIn, fOut, mod, folder, name))