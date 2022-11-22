import maya.cmds as cmds

def create_shader(name, node_type="lambert"):
    material = cmds.shadingNode(node_type, name=name, asShader=True)
    sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
    return material, sg

def smooth():
    #Dupliquer la base
    obj = cmds.ls (sl = True)
    dupli = cmds.duplicate (obj, rr = True)

    #Smooth la base
    listMesh = cmds.listRelatives (dupli, ad = True, type = "mesh")
    for mesh in listMesh :
        cmds.polySmooth (mesh, sdt = 2, ofb = 1, dv=  2)
        
    #Rename base to high       
    listAll = cmds.listRelatives (dupli, ad = True) + dupli
    for child in listAll :
        cmds.rename (child, child.replace("_geo", "_high").replace("_grp", "_high"))

    #DeleteHistory
    cmds.delete (all = True, ch = True)
        
    #Duplique high to id
    dupli2 = cmds.duplicate (dupli[0].replace("_grp", "_high"), rr = True)

    #Rename high to id 
    listAll = cmds.listRelatives (dupli2, ad = True, path = True) + dupli2
    for child in listAll :
        newName = cmds.rename (child, child.split("|")[-1].replace("_high", "_id"))
        if newName.endswith("1") :
            cmds.rename (newName, newName[:-1])

    #Geo to shaders
    colorByLetters = {"A":[1, 0, 0], "B":[0, 1, 0], "C":[0, 0, 1], "D":[1, 1, 0], "E":[1, 0, 1], "F":[0, 1, 1], "G":[1, 0.5, 0], "H":[1, 0, 0.5], "I":[0.5, 1, 0], "J":[0, 1, 0.5], "K":[0.5, 0, 1], "L":[0, 0.5, 1]}        
    for letters in colorByLetters.keys() :
        id = cmds.ls ("*_{}_*_id".format(letters))
        material, sg = create_shader ("{}_lambert".format(letters))
        cmds.setAttr ("{}.color".format(material), *colorByLetters[letters], type = "double3")
        cmds.select(id, r = True)
        cmds.sets(id, e = True, forceElement = sg)