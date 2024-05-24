import maya.cmds as cmds

def shad():

	cmds.select("MOD_grp", hierarchy=True)
	geos = cmds.listRelatives(shapes=True, children=True)

	shadingGrps = []
	correspondence = dict()
	
	#list materials on geo
	for geo in geos:

		sg = cmds.listConnections(geo, type='shadingEngine')
		print(geo, sg)
		for s in sg:
			shadingGrps.append(s)

	#export materials to file
	print(shadingGrps)
	cmds.select(shadingGrps, replace=True, noExpand=True)
	#cmds.file("E:/TEST_projet/test.ma", type="mayaAscii", exportSelected=True)

	#Create correspondence between geo and mat

	#Find Arnold attr values

	#