import maya.cmds as cmds
import os

def checkWR():
	cmds.rename("C_Root_jnt", "c_root_jnt")
	cmds.rename("C_Ultimate_jnt", "c_ultimate_jnt")
	cmds.rename("C_Global_ctrl", "c_global_0001_ctrl")
	cmds.rename("C_Root_ctrl", "c_root_0001_ctrl")

def updateWR():
	
	root = cmds.objExists("C_Root_jnt")
	if root == True:
		checkWR()

	#Clear Selection

	cmds.select(clear=True)

	#selectionner la reference
	ref = cmds.ls(references=True)
	cmds.select('*:MOD_grp')
	pfile = cmds.listRelatives(parent=True)


	#Unload la ref
	#Supprimer les edits
	#Reload la ref

	cmds.file(unloadReference=ref[0])
	cmds.referenceEdit(ref[0],failedEdits=True, successfulEdits=True,  removeEdits=True)
	cmds.file(loadReference=ref[0])

	#Changer la reference
	#Recuperer la version de la ref

	path = cmds.referenceQuery(ref[0], filename = True)
	directory, rfile = os.path.split(path)
	print(rfile)
	name = rfile.split("_")
	print(name)
	del name[-1]
	name = "_".join(name)
	print(name)
	verExt = rfile.split("_")[-1]
	version = verExt.split(".")[0]
	res_str = version.replace('v', '')
	verNb =  int(res_str)
	verNb+=1
	verNb = str(verNb)
	verNb = verNb.rjust(4, '0')

	#Nouveau nom et chemin d'acces

	newName = name+"_v"+verNb+".abc"
	newPath = os.path.join(directory, newName)
	print(newName)

	#Verifier si la nouvelle ref existe

	if os.path.exists(newPath):
		cmds.file(newPath, loadReference=ref[0])
	else:
		newPath = cmds.fileDialog2(fileMode=1)
		print(newPath)
		cmds.file(newPath, loadReference=ref[0])
		
	#Reparenter la nouvelle ref

	cmds.parent('*:MOD_grp', pfile[0])

	#Rebind skin

	cmds.select(clear=True)
	cmds.select('*:MOD_grp', 'c_root_jnt')
	cmds.bindSkin(tsb=True)

	#Clear Selection

	cmds.select(clear=True)