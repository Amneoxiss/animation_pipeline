import maya.cmds as cmds
import os
import json

def importPlan():

	#create new file
	cmds.file(force=True, new=True)
	shotFolder = cmds.fileDialog2(fileMode=3)[0]	
	shotFolder = os.path.normpath(shotFolder)

	#get seq and shot
	seq = shotFolder.split(os.sep)[-2]
	shot = shotFolder.split(os.sep)[-1]

	folder = os.path.join(shotFolder, "RENDU")
	cmds.file(rename="{0}/{1}{2}RENDU_v0001.ma".format(folder, seq, shot))
	cmds.file(save=True, type='mayaAscii')

	#Import anim config
	jsonPath = os.path.join(shotFolder, "ANIMATION/_Publish/{0}{1}.json".format(seq, shot)).replace("\\","/")
	with open(jsonPath, 'r') as f:
		fRange = json.load(f)

	print(fRange)

	fIn = fRange.get("In")
	fOut = fRange.get("Out")
	fps = fRange.get("fps")
	
	#Apply config to scene
	cmds.currentUnit(time=fps)
	cmds.playbackOptions(animationStartTime=fIn)
	cmds.playbackOptions(min=fIn)
	cmds.playbackOptions(animationEndTime=fOut)
	cmds.playbackOptions(max=fOut)
	cmds.currentTime(fIn)

	
	#Trouver les Abc de l'anim
	abcAnimF = os.path.join(shotFolder, "ANIMATION/_Publish/Alembic")
	abcAnims = os.listdir(abcAnimF)
	for abcAnim in abcAnims:
		print(abcAnim)
		abc = os.path.join(abcAnimF, abcAnim)
		abcNspace = os.listdir(abc)
		abc = os.path.join(abc, abcNspace[0])

		#Referencer les alembics
		cmds.file(abc, reference=True, namespace=abcAnim)