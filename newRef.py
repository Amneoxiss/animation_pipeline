import maya.cmds as cmds
import os

#REFERENCE WITH THE GOOD NAMESPACE

def ref():

	multipleFilters = "Geo Files (*.ma *.mb *.abc);;Maya ASCII (*.ma);;Maya Binary (*.mb);;Alembic (*.abc);;All Files (*.*);;"
	newRef = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, fileMode=1)
	newRef = newRef[0]

	#find namespace

	folder, file = os.path.split(newRef)
	file = file.split("_")
	nb = 1
	nb = str(nb)
	nb = nb.rjust(2, '0')

	baseName = file[0] + "_" + file [1] + "_"
	nSpace =  baseName + nb

	while cmds.namespace(exists=":*:{0}".format(nSpace))==True or cmds.namespace(exists=nSpace)==True:
		nb = int(nb)
		nb+=1
		nb = str(nb)
		nb = nb.rjust(2, '0')
		print(nb)
		nSpace = baseName + nb

	else:
		pass

	cmds.file(newRef, reference=True, namespace=nSpace)
	
	'''
	#Check for proxy
	proxyName = file[1]+"Proxy"
	print(proxyName)
	proxyFolder = folder.replace(file[1], proxyName)
	print(proxyFolder)

	if os.path.exists(proxyFolder)==True:
		cmds.confirmDialog(title="Warning", message="Found a proxy for this asset. Would you like to add it", button=['Yes','No'], defaultButton='Yes', cancelButton='No')
		
	else:
		print("None")
	
	'''