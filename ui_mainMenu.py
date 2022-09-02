import pymel.core as pm

def wipAlert():

	pm.confirmDialog(title="Assets Manager", message="Work in progress", button=['OK'], defaultButton='OK')

def ui():

	main_window = pm.language.melGlobals['gMainWindow']

	menu_obj = 'Pipeline'
	menu_label = 'Pipeline 3IS'

	if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
		pm.deleteUI(pm.menu(menu_obj, e=True, deleteAllItems=True))

	pipeline_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)

	#ASSETS MANAGER
	pm.menuItem(label="ASSETS MANAGER [WIP]", command='ui_mainMenu.wipAlert()')

	#Create new reference
	pm.menuItem(label="Reference", command='import newRef; newRef.ref()')

	#MOD tools
	pm.menuItem(label="Mod tools", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="Sanity Check", command='from modelChecker.modelChecker_UI import modelCheckerUI; modelCheckerUI.show_UI()')
	pm.menuItem(label="Publish mod", command='from mod.publish import publishMod; reload(publishMod); publishMod.pMod()')

	#RIGGING tools
	pm.menuItem(label="Rigging tools", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="Create world rig", command='from rig.worldRig import worldRig; worldRig.worldRig()')
	pm.menuItem(label="Update world rig", command='from rig.worldRig import updateWorldRig; updateWorldRig.updateWR()')	
	pm.menuItem(label="Publish rig", command='from rig.publish import publishRig; publishRig.pRig()')
	pm.menuItem(label="Create Ctrl", command='from rig.bsControls import bs_controlsUI; bsCon = bs_controlsUI.BSControlsUI(); bsCon.bsControlsUI()')
	pm.menuItem(label="Lock geo", command="from rig.lockGeo import ui_lockGeo; reload(ui_lockGeo); lg = ui_lockGeo.LockGeoDialog; lg.show_ui()")
	
	#Set tools
	pm.menuItem(label="Set tools", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="Update Set", command='import updateSet; updateSet.update()')
	pm.menuItem(label="Publish Set", command='import publishSet; publishSet.pSet()')

	#Animation tools
	pm.menuItem(label="Animation", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="Create new scene", command='from anim.create import createNewAnimShot; createNewAnimShot.createScene()')
	pm.menuItem(label="Playblast", command='from anim.playblast import ui_playblast; ui_playblast.main()')
	pm.menuItem(label="Export animation [WIP]", command='ui_mainMenu.wipAlert()')

	#Shading tools
	pm.menuItem(label="Shading", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="Export shaders [WIP]", command='ui_mainMenu.wipAlert()')
	pm.menuItem(label="Relink shaders [WIP]", command='ui_mainMenu.wipAlert()')
	pm.menuItem(label="Publish mod lookdev", command='import publishLdev; publishLdev.pLdev()')

	#FX tools
	pm.menuItem(label="FX", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="NONE [WIP]", command='ui_mainMenu.wipAlert()')

	#Lighting Tools
	pm.menuItem(label="Lighting", subMenu=True, parent=pipeline_menu, tearOff=False)
	pm.menuItem(label="Publish light rig [WIP]", command='ui_mainMenu.wipAlert()')
	pm.menuItem(label="Import light rig [WIP]", command='ui_mainMenu.wipAlert()')
	pm.menuItem(label="Publish for rendering", command='import publishRendering; publishRendering.pRendering()')