import maya.cmds as cmds
from helpers import getSceneName, version_increment
import os

def publish(ext, pubFolder):

	path = cmds.file(query=True, sceneName=True)
	directory, filename = os.path.split(path)
	directory = os.path.join(directory, pubFolder)

	if os.path.exists(directory):
		pass
	else:
		os.makedirs(directory)

	files = os.listdir(directory)

	if not files :
		name = getSceneName.getName(filename)
		name = name+"_pb_v0001.{0}".format(ext)
		newPath = os.path.join(directory, name).replace("\\", "/")

	else :
		filename = files[-1]

		name = getSceneName.getName(filename)
		verNb = version_increment.inc(filename)

		#Path to publish
		name = name+"_v"+verNb+"."+ext
		newPath = os.path.join(directory, name).replace("\\", "/")

	return newPath, path