import maya.cmds as cmds
import os

def update():
    
    cmds.select(clear=True)

    #lister les refs

    refs = cmds.ls(references=True)

    #recuperer la version de la ref

    for ref in refs:
        path = cmds.referenceQuery(ref, filename = True)
        directory, rfile = os.path.split(path)
        name = rfile.split("_")[0]
        verExt = rfile.split("_")[-1]
        version = verExt.split(".")[0]
        res_str = version.replace('v', '')
        verNb =  int(res_str)
        verNb+=1
        verNb = str(verNb)
        verNb = verNb.rjust(4, '0')

        #Nouveau nom et chemin d'acces

        newName = name+"_pb_v"+verNb+".mb"
        newPath = os.path.join(directory, newName)

        #Verifier si la nouvelle ref existe

        if os.path.exists(newPath):
            cmds.file(newPath, loadReference=ref)
        else:
            pass

    #clear selection

    cmds.select(clear=True)

    #Fin d'udpate

    cmds.confirmDialog(title="Assets Manager", message="Update Set done !", button=['OK'], defaultButton='OK')