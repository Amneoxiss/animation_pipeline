import maya.cmds as cmds

def worldRig():
	
	#ClearSelection

	cmds.select(clear=True)

	#Trouver la BB
	slc = cmds.select('*:MOD_grp')
	bbox = cmds.exactWorldBoundingBox()
	slc = cmds.select(clear=True)
	bbox = [abs(ele) for ele in bbox]   

	#Creer les joint Root et Ultimate en fonction de la BB
	cmds.joint(name='c_root_jnt', p=(0,0,0))
	cmds.joint(name='c_ultimate_jnt', p=(0,bbox[4],0))
	cmds.select('c_root_jnt')
	cmds.group(name='RIG_grp')
	cmds.setAttr('RIG_grp.visibility', 0)

	#Skin des joints a la geo
	cmds.select(clear=True)
	cmds.select('*:MOD_grp', 'c_root_jnt')
	cmds.bindSkin(tsb=True)

	#Trouver le scale des controleurs
	#On retire les valeurs Y de la bounding box puis on trie les valeurs restantes 
	bbox.remove(bbox[1])
	bbox.remove(bbox[3])
	bbox.sort()

	#Creer le Controleur Global, lui donner les bonnes dimensions puis FT et DH
	cmds.circle(n='c_global_0001_ctrl', nr=(0,1,0), c=(0,0,0))
	cmds.scale(bbox[-1]*2, 1, bbox[-1]*2)
	cmds.delete(constructionHistory = True)
	cmds.makeIdentity(apply=True, scale=True)
	cmds.group(name="c_global_0001_off")

	#Creer le Controleur Root, lui donner les bonnes dimensions puis FT et DH
	cmds.circle(n='c_root_0001_ctrl', nr=(0,1,0), c=(0,0,0))
	cmds.scale(bbox[-1]*1.5, 1, bbox[-1]*1.5)
	cmds.delete(constructionHistory = True)
	cmds.makeIdentity(apply=True, scale=True)
	cmds.group(name="c_root_0001_off")
	cmds.parent('c_root_0001_off', 'c_global_0001_ctrl')

	cmds.select('c_global_0001_off')
	cmds.group(name='CTRL_grp')

	#Creer la contrainte entre le ctrl et le joint
	cmds.parentConstraint('c_root_0001_ctrl', 'c_root_jnt', maintainOffset=True, weight=1)

	#Creer un groupe Global
	cmds.select('CTRL_grp', 'RIG_grp', '*:MOD_grp')
	cmds.group(name='Asset_grp')
