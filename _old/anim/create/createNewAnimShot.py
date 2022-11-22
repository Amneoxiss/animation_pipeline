import maya.cmds as cmds
import os

def createScene():

	#create new file
	shotFolder = cmds.fileDialog2(fileMode=3)[0]	
	shotFolder = os.path.normpath(shotFolder)
	
	#get seq and shot
	seq = shotFolder.split(os.sep)[-2]
	shot = shotFolder.split(os.sep)[-1]

	folder = os.path.join(shotFolder, "ANIMATION")
	name = "{1}_{2}_anim_v0001.ma".format(folder, seq, shot)
	directory = os.path.join(folder, name)

	files = os.listdir(folder)

	if not files:
		newScene(directory, seq, shot)

	else:
		result = cmds.confirmDialog(title="New scene", message="Are You Sure ?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')

		if result == 'No':
			pass

		else:
			newScene(directory, seq, shot)
	

def newScene(directory, seq, shot):

	cmds.file(force=True, new=True)
	cmds.file(rename=directory)
	cmds.file(save=True, type='mayaAscii')

	#INIT value

	fps = 'pal'
	fIn = 1001
	fOut = 1200

	Rw = 1998
	Rh = 1080
	aspectR = float(Rw)/float(Rh)
	pixelA = 1.0

	#Reference camera and set
	cmds.file("Z:/PROJETS/Mesange/02_Prod/01_Assets/04_Cam/CameraA/RIG/_Publish/cam_renderCam_rig_pb_v0004.mb", reference=True, namespace="{0}_{1}".format(seq, shot))
	cmds.file("Z:/PROJETS/Mesange/02_Prod/02_Set/exterieur/_Publish/set_exterieur_pb_v0011.mb", reference=True, namespace="set_exterieur")

	#Assign values
	cmds.currentUnit(time=fps)
	cmds.playbackOptions(animationStartTime=fIn)
	cmds.playbackOptions(min=fIn)
	cmds.playbackOptions(animationEndTime=fOut)
	cmds.playbackOptions(max=fOut)
	cmds.currentTime(fIn)
	cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 0)
	cmds.setAttr("defaultResolution.width", Rw)
	cmds.setAttr("defaultResolution.height", Rh)
	cmds.setAttr("defaultResolution.deviceAspectRatio" , aspectR)
	cmds.setAttr("defaultResolution.pixelAspect", pixelA)

	cmds.file(save=True)


if __name__ == "__main__":
	createScene()
