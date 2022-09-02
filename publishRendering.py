import maya.cmds as cmds
import os

def pRendering():

	path = cmds.file(query=True, sceneName=True)
	directory, filename = os.path.split(path)
	directory = os.path.join(directory, "_Publish")
	files = os.listdir(directory)

	if not files :
	    name = filename.split("_")[0]
	    name = name+"_pb_v0001.mb"
	    newPath = os.path.join(directory, name)

	else :
	    lastPublish = files[-1]
	    print(lastPublish)
	    
	    name = filename.split("_")[0]
	    verExt = lastPublish.split("_")[-1]
	    version = verExt.split(".")[0]
	    res_str = version.replace('v', '')
	    verNb =  int(res_str)
	    verNb+=1
	    verNb = str(verNb)
	    verNb = verNb.rjust(4, '0')

	    #Path to publish
	    name = name+"_pb_v"+verNb+".mb"
	    newPath = os.path.join(directory, name)

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

	#re open working scene
	cmds.file(save=True)

	#end
	cmds.select(clear=True)
	cmds.confirmDialog(title="Publish", message="Ready for rendering !", button=['Ok'], defaultButton="Ok")
