import maya.cmds as cmds
import sys
import maya.mel as mel
sys.path.append('../../modules')
from modules import getSceneName, increment
import os

def publish():

	cmds.select(clear = True)

	path = cmds.file(query = True, sceneName = True )
	print(path)

	directory, filename = os.path.split(path)
	print (directory, filename)

	directory = directory.replace(r"03_Animation/01_Shots_plans", "05_Rendu")
	shotname = filename.split("_")[0]
	filename = shotname+"_RENDER"
	newpath = os.path.join(directory,"_Export", filename)
	print(newpath)

	#Change settings before export
	camName = shotname+"Main_camShape"
	cmds.setAttr("{}.overscan".format(camName),1)
	cmds.setAttr("{}.displayGateMask".format(camName),0)
	cmds.setAttr("{}.displayResolution".format(camName),0)


	viewports = [p for p in cmds.getPanel(allPanels = True) if "modelPanel" in p]
	for viewport in viewports :
		cmds.modelEditor (viewport, e = True, allObjects = 0)
		cmds.modelEditor (viewport, e = True, polymeshes = True)
		cmds.modelEditor (viewport, e = True, displayTextures = True)

	cmds.playblast (format = "image", filename = newpath, sequenceTime = 0, clearCache = 1, viewer = 0, showOrnaments = 0, fp = 4, percent = 100, compression = "png", widthHeight =[1998, 1080])

	#Reset Settings
	cmds.setAttr("{}.overscan".format(camName),1.3)
	cmds.setAttr("{}.displayGateMask".format(camName),1)
	cmds.setAttr("{}.displayResolution".format(camName),1)

	for viewport in viewports :
		cmds.modelEditor (viewport, e = True, allObjects = 1)
		cmds.modelEditor (viewport, e = True, displayTextures = False)

	print("Published !")

def wip():

	cmds.select(clear = True)

	path = cmds.file(query = True, sceneName = True)
	print(path)

	directory, filename = os.path.split(path)
	directory = os.path.join(directory,"_playblast")
	print (directory, filename)

	if not os.path.exists(directory):
		os.makedirs(directory)

	files = os.listdir(directory)
	seq = filename.split("_")[0]
	shot = filename.split("_")[1]
	shotname = seq+"_"+shot

	if not files: 
		filename = shotname+"_anim"+"_v0001"

	else:
		filename = files[-1]
		verNb = increment.inc(filename)
		filename = shotname + "_anim_v"+verNb
		

	newpath = os.path.join(directory, filename)
	print(newpath)

	#Change settings before export
	camName = shotname+":RenderCam_camShape"
	print(camName)
	
	mel.eval('setNamedPanelLayout("Single Perspective View")')
	cmds.lookThru('perspView', camName)

	cmds.setAttr("{}.overscan".format(camName),1)
	cmds.setAttr("{}.displayGateMask".format(camName),0)
	cmds.setAttr("{}.displayResolution".format(camName),0)
	cmds.setAttr("{}.displayFieldChart".format(camName),0)
	cmds.setAttr("{}.displaySafeAction".format(camName),0)
	cmds.setAttr("{}.displaySafeTitle".format(camName),0)
	cmds.setAttr("{}.displayFilmPivot".format(camName),0)
	cmds.setAttr("{}.displayFilmOrigin".format(camName),0)


	

	viewports = [p for p in cmds.getPanel(allPanels = True) if "modelPanel" in p]
	for viewport in viewports :
		cmds.modelEditor (viewport, e = True, allObjects = 0)
		cmds.modelEditor (viewport, e = True, polymeshes = True)
		cmds.modelEditor (viewport, e = True, displayTextures = True)
		cmds.modelEditor (viewport, e = True, particleInstancers = True)
		cmds.modelEditor (viewport, e = True, pluginShapes = True)

	mel.eval('generateAllUvTilePreviews')

	cmds.playblast (format = "qt", filename = newpath, sequenceTime = 0, clearCache = 1, viewer = 0, showOrnaments = 0, fp = 4, percent = 100, compression = "png", widthHeight =[1998, 1080])

	#Reset Settings
	cmds.setAttr("{}.overscan".format(camName),1.3)
	cmds.setAttr("{}.displayGateMask".format(camName),1)
	cmds.setAttr("{}.displayResolution".format(camName),1)

	for viewport in viewports :
		cmds.modelEditor (viewport, e = True, allObjects = 1)
		cmds.modelEditor (viewport, e = True, displayTextures = False)

	print("WIP !")