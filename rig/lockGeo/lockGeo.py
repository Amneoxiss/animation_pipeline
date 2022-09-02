import maya.cmds as cmds

def lockSelected():

	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 1)
		cmds.setAttr(geo+".overrideDisplayType", 2)

def unlockSelected():

	geos = cmds.ls(selection=True)

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 0)
		cmds.setAttr(geo+".overrideDisplayType", 0)

def lockAll():

	geos = selectAll()

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 1)
		cmds.setAttr(geo+".overrideDisplayType", 2)

	cmds.select(clear=True)

def unlockAll():

	geos = selectAll()

	for geo in geos:
		cmds.setAttr(geo+".overrideEnabled", 0)
		cmds.setAttr(geo+".overrideDisplayType", 0)

	cmds.select(clear=True)

def selectAll():
    
    types = cmds.ls(type="shape")
    geos = []

    for type in types:
        t = cmds.nodeType(type)
        if t == "mesh":
            trans = cmds.listRelatives(type, parent=True)
            geos.append(trans[0])
        else:
            pass
        
    return(geos)