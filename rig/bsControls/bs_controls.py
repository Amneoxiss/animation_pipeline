'''

Control Curves Tool made by Brandon Schaal

Easily create control curves, change control curve colors, and replace control curve shapes. Changes colors on the shape level to 
avoid all children of the controls inheriting drawing overrides, resets the colors at both shape and transform levels, and can replace 
multiple shapes on controllers with either one or an equal amount of replacement shapes. 

This tool has a list of 35 different control shapes that can be created at selected objects in world space or as a parent/child of the objects. 
There is also the option to just make the control at the origin, as well as to replace suffixes or name controls as needed and evem change the 
thickness of created controls. New shapes can easily be added to the BSControlsData class dictionary and text scroll list  as needed. All control 
curves are made linear with many CVs to create complex shapes while only using one shape node per control curve (with one exception for the Gear curve). 
A function is provided below to easily get the tuple list of all CV positions of a control curve you wish to add.

'''
import sys
import maya.cmds as cmds

sys.path.append("../../modules")
from modules import toCamelCase

class BSControlsUtils():
    # Function for creating a new control curve name.
    def bsNameCurve(self, curve, name):
        if name == '':
            newName = toCamelCase.camelCase(curve[0])

        else:
            newName = name.replace(" ", "_")
            newName = newName.replace("-", "_")
            newName = newName.split("_")
            

            if newName[0] == "ik" or newName[0] == "fk":
                prefix = newName[0]
                del newName[0]
                newName = '_'.join(newName)
                newName = toCamelCase.camelCase(newName)
                newName = prefix + "_" + newName
            else:
                newName = '_'.join(newName)
                newName = toCamelCase.camelCase(newName)

        return newName

    def bsGetObjName(self, obj, curve, name):
            objName = obj.split("_")
            pos = objName[0]
            newName = objName[1]

            if pos == "c" or pos == "r" or pos == "l":
                pass
            
            else:
                pos = "c"
                newName = self.bsNameCurve(curve, name)

            return pos, newName


    # Function to draw nurbs curves from dictionary data and user input.
    def bsDrawCurve(self, curve, thickness):
        # Exception for Circle shape.
        if curve == 'Circle':
            crv = cmds.circle(d=3, r=2, nr=[0,1,0], ch=False)
        else:
            crv = cmds.curve(d=1, p=BSControlsData.cvTuples[curve])

        # Exception for adding an additional shape node to the Gear curve.
        if curve == 'Gear':
            circle = cmds.circle(r=0.9, nr=[0,1,0])
            circleShape = cmds.listRelatives(circle, s=True)
            circleShape = cmds.rename(circleShape, crv + 'CircleShape')
            cmds.parent(circleShape, crv, add=True, s=True)
            cmds.delete(circle)

        # Only adjusting the lineWidth attribute only if a value greater than 1.0 is input.
        if thickness > 1.0:
            crvShape = cmds.listRelatives(crv, s=True)
            for c in crvShape:
                cmds.setAttr('%s.lineWidth'%(c), thickness)
        else:
            pass

        return crv

    # Function to move the control curve after drawing and renaming the curve.
    def bsCurvePosition(self, obj, curve, thickness, name):
        # Creating and naming curve.
        newName = self.bsNameCurve(curve, name)
        crv = self.bsDrawCurve(curve, thickness)
        crv = cmds.rename(crv, newName)

        # Matching positions with a parent constraint.
        const = cmds.parentConstraint(obj, crv)
        cmds. delete(const)

        return crv

    # Function to place the controls in proper hierarchies based on user input.
    def bsPlaceControls(self, button, curve, name, thickness):
        sel = cmds.ls(sl=True)

        # Parent Button
        if button == 'parent':
            if len(sel) < 1:
                cmds.error('Select at least 1 object.')

            for obj in sel:
                crv = self.bsDrawCurve(curve[0], thickness)
                pos, newName = self.bsGetObjName(obj, curve, name)

                if name == '':
                    grp = cmds.group(crv, name="{0}_{1}_ctrl_grp".format(pos, newName))
                    cmds.rename(crv, "{0}_{1}_ctrl".format(pos, newName))

                else:                    
                    newName = self.bsNameCurve(curve, name)
                    grp = cmds.group(crv, name="{0}_{1}_ctrl_grp".format(pos, newName))
                    cmds.rename(crv, "{0}_{1}_ctrl".format(pos, newName))

                const = cmds.parentConstraint(obj, grp)
                cmds. delete(const)


        # Child Button
        elif button == 'child':
            if len(sel) < 1:
                cmds.error('Select at least 1 object.')

            for obj in sel:
                crv = self.bsCurvePosition(obj, curve[0], thickness, name)

                objChild = cmds.listRelatives(obj, c=True, typ='transform')

                if objChild != None:
                    cmds.parent(objChild, crv)

                cmds.parent(crv, obj)

        # World Button
        elif button == 'world':
            if len(sel) < 1:
                cmds.error('Select at least 1 object.')

            for obj in sel:
                crv = self.bsCurvePosition(obj, curve[0], thickness, name)

        # Origin Button
        elif button == 'origin':
            crv = self.bsDrawCurve(curve[0], thickness)

            if name == '':
                name = curve[0].lower()
                name = name.replace(' ', '')
                cmds.rename(crv, name)
            else:
                name = name.replace(' ', '')
                cmds.rename(crv, name)

        #Center Button
        elif button == 'center' or button == 'left' or button == 'right':
            crv = self.bsDrawCurve(curve[0], thickness)
            newName = self.bsNameCurve(curve, name)

            if button == 'center':
                cmds.group(crv, name="c_{0}_ctrl_grp".format(newName))
                cmds.rename(crv, "c_{0}_ctrl".format(newName))

            if button == 'left':
                cmds.group(crv, name="l_{0}_ctrl_grp".format(newName))
                cmds.rename(crv, "l_{0}_ctrl".format(newName))

            if button == 'right':
                cmds.group(crv, name="r_{0}_ctrl_grp".format(newName))
                cmds.rename(crv, "r_{0}_ctrl".format(newName))

    # Function to set the color of the selected shapes.
    def bsSetIndex(self, color):
        sel = cmds.ls(sl=True, l=True)

        for objs in sel:
            # Getting and checking node type to act on shape level
            nType = cmds.nodeType(objs)

            if nType == 'transform':
                objs = cmds.listRelatives(objs, s=True)
            elif nType == 'shape':
                pass
            else:
                cmds.error('Selected object(s) is not a nurbs curve.')

            # Changing drawing override color on multiple shapes.
            for obj in objs:
                override = cmds.getAttr('%s.overrideEnabled'%(obj))
                if override == 0:
                    cmds.setAttr('%s.overrideEnabled'%(obj), 1)

                display = cmds.getAttr('%s.overrideDisplayType'%(obj))
                if display != 0:
                    cmds.setAttr('%s.overrideDisplayType'%(obj), 0)

                cmds.setAttr('%s.overrideColor'%(obj), color)

        cmds.select(d=True)  

    # Function to set the selected shapes display type.
    def bsSetDisplayType(self, display):
        sel = cmds.ls(sl=True, l=True)

        for objs in sel:
            # Getting and checking node type to act on shape level
            nType = cmds.nodeType(objs)

            if nType == 'transform':
                objs = cmds.listRelatives(objs, s=True)
            elif nType == 'shape':
                pass
            else:
                cmds.error('Selected object(s) is not a nurbs curve.')

            # Changing drawing override display type on multiple shapes.
            for obj in objs:
                override = cmds.getAttr('%s.overrideEnabled'%(obj))
                if override == 0:
                    cmds.setAttr('%s.overrideEnabled'%(obj), 1)

                cmds.setAttr('%s.overrideDisplayType'%(obj), display)

        cmds.select(d=True)

    # Function to reset the color of selected shapes.
    def bsResetColor(self, *args):
        sel = cmds.ls(sl=True, l=True)

        for objs in sel:
            # Resetting drawing overrides on transform level.
            override = cmds.getAttr('%s.overrideEnabled'%(objs))
            if override == 1:
                cmds.setAttr('%s.overrideEnabled'%(objs), 0)

            cmds.setAttr('%s.overrideColor'%(objs), 0)
            cmds.setAttr('%s.overrideDisplayType'%(objs), 0)

            # Getting and checking node type to act on shape level.
            nType = cmds.nodeType(objs)

            if nType == 'transform':
                shapes = cmds.listRelatives(objs, s=True)
            elif nType == 'shape':
                pass
            else:
                cmds.error('Selected object(s) is not a nurbs curve.')

            # Resetting drawing overrides on multiple shapes.
            for s in shapes:
                overrideShape = cmds.getAttr('%s.overrideEnabled'%(s))
                if overrideShape == 1:
                    cmds.setAttr('%s.overrideEnabled'%(s), 0)
                cmds.setAttr('%s.overrideColor'%(s), 0)
                cmds.setAttr('%s.overrideDisplayType'%(s), 0)

        cmds.select(d=True)

    # Function to load shapes into text fields with a button press and return the selection.
    def bsLoadShapes(self, textField):
        sel = cmds.ls(sl=True, l=True)

        niceSel = [s.split('|')[-1] for s in sel]
 
        text = ', '.join(niceSel)
        length = len(niceSel)

        # If more than one object is selected the text box will display how many shapes are loaded instead of names.
        if length > 1:
            cmds.textField(textField, e=True, tx='%d shapes loaded.'%(length))
        else:
            cmds.textField(textField, e=True, tx=text)

        return sel

    # Function to replace shape(s) with a loaded replacement(s).
    def bsReplaceShape(self, target, replacement, mirror):
        # Duplicating the replacement shape source.
        duplicate = cmds.duplicate(replacement, rr=True, rc=True, n='temp_CRV')

        # Unlocking attributes for parent constraint and freeze transforms.
        cmds.setAttr (duplicate[0] + '.tx', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.ty', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.tz', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.rx', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.ry', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.rz', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.sx', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.sy', l = 0, k = 1)
        cmds.setAttr (duplicate[0] + '.sz', l = 0, k = 1)

        # Parenting duplicate to world and deleting the children
        duplicatePar = cmds.listRelatives(duplicate, p=True)
        if duplicatePar != None:
            duplicate = cmds.parent(duplicate, w=True)
            
        children = cmds.listRelatives(duplicate, c=True, f=True)
        for child in children:
            c = child.lower()
            if 'shape' in c:
                pass
            else:
                cmds.delete(child)

        # Matching the position of the target
        if mirror == True:
            grp = cmds.group(em=True, w=True, n='mirror_GRP')
            cmds.parent(duplicate, grp)
            cmds.setAttr('%s.scaleX'%(grp), -1.0)
            cmds.parent(duplicate, w=True)
            cmds.delete(grp)
        else:
            const = cmds.parentConstraint(target, duplicate)
            cmds.delete(const)

        # Parenting the duplicate to target shape's parent.
        cmds.parent(duplicate, target)
        cmds.makeIdentity(duplicate, apply=True, t=1, r=1, s=1)

        # Getting the shape nodes and deleting the target's current shape
        duplicateShape = cmds.listRelatives(duplicate, s=True)
        targetShape = cmds.listRelatives(target, s=True)
        targetNice = target.split('|')[-1] + 'Shape'
        cmds.delete(targetShape)

        # Parenting the duplicate shapes to target transform and renaming.
        for shape in duplicateShape:
            shape = cmds.rename(shape, targetNice)
            cmds.parent(shape, target, add=True, s=True)

        # Deleting duplicate.
        cmds.delete(duplicate)

    def bsMirror(self):
        ctrl = cmds.ls(selection=True)
        ctrlN = str(ctrl[0])
        ctrlN = ctrlN.split("_")

        #check for control or offset group
        if ctrlN[-1] == "ctrl":
            ctrl = cmds.listRelatives(parent=True)
            cmds.select(ctrl, replace=True)
        else:
            pass

        cmds.select(clear=True)

        #Create new group to duplicate
        cmds.group(empty=True, name="toDuplicate_grp", relative=False, world=True)
        cmds.parent(ctrl, "toDuplicate_grp")

        #Duplicate group
        cmds.duplicate("toDuplicate_grp", name="Duplicate_grp")
        cmds.select("Duplicate_grp")

        #Mirror by scaling x -1
        cmds.scale( -1 , 1, 1)

        #Rename Duplicate
        nCtrls = cmds.listRelatives(allDescendents=True, path=True)

        for nCtrl in nCtrls:
            name = nCtrl.split("|")[-1]
            side = name.split("_")
            if side[0] == "l":
                side[0] = "r"
                newName = "_".join(side)
                cmds.rename(nCtrl, nCtrl.split("|")[-1].replace(name, newName))
            else:
                side[0] = "l"
                newName = "_".join(side)
                cmds.rename(nCtrl, nCtrl.split("|")[-1].replace(name, newName))

        #Unparent Base
        cmds.parent(ctrl, world=True)

        #Delete toDuplicate group
        cmds.delete("toDuplicate_grp")

        #Unparent Duplicate
        cmds.parent(newName, world=True)

        #Delete Duplicate group
        cmds.delete("Duplicate_grp")

    
    def bsParentCtrlJnt(self):
        sels = cmds.ls(selection=True)

        for sel in sels:
            selN = sel.split("_")

            if selN[-1] == "ctrl":
                ctrl = cmds.listRelatives(parent=True)
                cmds.select(ctrl, replace=True)

            elif selN[-1] == "jnt":
                jnt = sel
                
            else:
                ctrl = sel

        const = cmds.parentConstraint(jnt, ctrl)
        cmds.delete(const)

class BSControlsData():
    '''
    If you wish to add more control curve options to the menu, simply add a new name into the "controlNames" list and a corresponding key in the dictionary
    with the list of tuples for CV coordinates. To easily get the list of tuples for a controller, select all of the CVs of a linear nurbs curve and run 
    the following script in a Python tab in the script editor. Then, select "tupleList" in the script editor and press Ctrl + Enter. You can copy paste 
    the printout into a new dictionary key at the bottom of the list.

    sel = cmds.ls(sl=True)
    trans = cmds.xform(sel, q=True, t=True)
    list = [trans[i:i+3] for i in range(0, len(trans), 3)]
    tupleList = [tuple(i) for i in list]
    '''

    # List of all control curve names.
    controlNames = ['Circle', 'Half Circle', 'Square', 'Triangle', 'Sphere', 'Half Sphere','Box', 'Pyramid', 'Diamond', 'Circle Pin','Square Pin', 
        'Sphere Pin', 'Circle Dumbbell', 'Square Dumbbell', 'Sphere Dumbbell', 'Cross', 'Cross Thin', 'Locator', 'Four Arrows', 'Four Arrows Thin',
        'Curved Four Arrows', 'Curved Four Arrows Thin', 'Two Arrows', 'Two Arrows Thin', 'Curved Two Arrows', 'Curved Two Arrows Thin', 'One Arrow', 
        'One Arrow Thin', 'Circle One Arrow',  'Circle Two Arrows', 'Circle Three Arrows', 'Circle Four Arrows', 'Sphere Four Arrows', 'Gear']

    # Control curve CV tuples dictionary.
    cvTuples = {}

    # Control curve CV dictionary keys.
    cvTuples['Half Circle'] = [
        (1.2246467991473532e-16, 1.2246467991473532e-16, -2.0), 
        (-0.3901806440322564, 1.2011155542966555e-16, -1.9615705608064609), 
        (-0.7653668647301793, 1.1314261122877003e-16, -1.8477590650225735), 
        (-1.1111404660392044, 1.0182565992946028e-16, -1.6629392246050905), 
        (-1.414213562373095, 8.659560562354932e-17, -1.414213562373095), 
        (-1.6629392246050902, 6.80377307569005e-17, -1.1111404660392044), 
        (-1.8477590650225733, 4.6865204053262986e-17, -0.7653668647301796), 
        (-1.9615705608064604, 2.3891673840167793e-17, -0.3901806440322566), 
        (-1.9999999999999996, 1.4296954280543742e-32, -2.3348698237725095e-16), 
        (-1.0, -1.0182565992946023e-16, 1.0736898889973645e-06), 
        (-2.334869823772509e-16, -1.2246467991473525e-16, 4.444297557526511e-06), 
        (1.0, -1.1314261122876998e-16, 2.9218882460213536e-06), 
        (1.9999999999999982, -3.1292342698629875e-32, 5.1104273853354e-16), 
        (1.961570560806459, 2.3891673840167737e-17, -0.39018064403225566), 
        (1.847759065022572, 4.68652040532629e-17, -0.7653668647301782), 
        (1.662939224605089, 6.80377307569004e-17, -1.1111404660392028), 
        (1.4142135623730938, 8.659560562354922e-17, -1.4142135623730931), 
        (1.1111404660392035, 1.0182565992946014e-16, -1.6629392246050883), 
        (0.7653668647301792, 1.1314261122876988e-16, -1.847759065022571), 
        (0.3901806440322567, 1.2011155542966538e-16, -1.9615705608064582), 
        (7.330873434585712e-16, 1.2246467991473515e-16, -1.9999999999999973)
    ]

    cvTuples['Square'] = [
        (-2.001501540839854, 0.0, -2.001501540839854),
        (-2.001501540839854, 0.0, 2.001501540839854),
        (2.001501540839854, 0.0, 2.001501540839854),
        (2.001501540839854, 0.0, -2.001501540839854),
        (-2.001501540839854, 0.0, -2.001501540839854)
    ]
    cvTuples['Triangle'] = [
        (-2.001501540839854, 0.0, 2.001501540839854),
        (0.0, 0.0, -2.001501540839854),
        (2.001501540839854, 0.0, 2.001501540839854),
        (-2.001501540839854, 0.0, 2.001501540839854)
    ]
    cvTuples['Sphere'] = [
        (0.0, 2.001501540839854, 0.0),
        (-9.331221744602883e-09, 1.9768597796103284, 0.3131038753308959),
        (-1.843267699523828e-08, 1.903541130260558, 0.6184980664640812),
        (-2.708025942441291e-08, 1.7833509413547823, 0.9086628426976106),
        (-3.5061033711582e-08, 1.619248777234614, 1.1764531908237743),
        (-4.217849039619503e-08, 1.4152752878617791, 1.4152754071605675),
        (-4.82573740850274e-08, 1.176453071524986, 1.619249015832191),
        (-5.314799968465514e-08, 0.9086627233988221, 1.7833511799523587),
        (-5.672994644226307e-08, 0.6184979471652929, 1.9035413688581349),
        (-5.891501246721531e-08, 0.3131036367333192, 1.9768600182079052),
        (-5.964939417957824e-08, 0.0, 2.001501779437431),
        (-5.891501246721531e-08, -0.3131036367333192, 1.9768600182079052),
        (-5.672994644226307e-08, -0.6184979471652929, 1.9035413688581349),
        (-5.314799968465514e-08, -0.9086627233988221, 1.7833511799523587),
        (-4.82573740850274e-08, -1.176453071524986, 1.619249015832191),
        (-4.217849039619503e-08, -1.4152752878617791, 1.4152754071605675),
        (-3.5061033711582e-08, -1.619248777234614, 1.1764531908237743),
        (-2.708025942441291e-08, -1.7833509413547823, 0.9086628426976106),
        (-1.843267699523828e-08, -1.903541130260558, 0.6184980664640812),
        (-9.331221744602883e-09, -1.9768597796103284, 0.3131038753308959),
        (0.0, -2.001501540839854, 0.0),
        (0.0, -1.9768597796103284, -0.31310399462968425),
        (0.0, -1.903541130260558, -0.6184983050616579),
        (0.0, -1.7833509413547823, -0.9086631409445814),
        (0.0, -1.619248777234614, -1.1764536680189277),
        (0.0, -1.4152752878617791, -1.4152760036545093),
        (0.0, -1.176453071524986, -1.6192494930273444),
        (0.0, -0.9086627233988221, -1.7833517764463007),
        (0.0, -0.6184979471652929, -1.903542084650865),
        (0.0, -0.3131036367333192, -1.9768607340006352),
        (0.0, 0.0, -2.001502495230161),
        (0.0, 0.3131036367333192, -1.9768607340006352),
        (0.0, 0.6184979471652929, -1.903542084650865),
        (0.0, 0.9086627233988221, -1.7833517764463007),
        (0.0, 1.176453071524986, -1.6192494930273444),
        (0.0, 1.4152752878617791, -1.4152760036545093),
        (0.0, 1.619248777234614, -1.1764536680189277),
        (0.0, 1.7833509413547823, -0.9086631409445814),
        (0.0, 1.903541130260558, -0.6184983050616579),
        (0.0, 1.9768597796103284, -0.31310399462968425),
        (0.0, 2.001501540839854, 0.0),
        (-0.31310393498029004, 1.9768597796103284, 0.0),
        (-0.6184981261134754, 1.903541130260558, 0.0),
        (-0.908662961996399, 1.7833509413547823, 0.0),
        (-1.1764533101225625, 1.619248777234614, 0.0),
        (-1.4152756457581444, 1.4152752878617791, 0.0),
        (-1.6192491351309795, 1.176453071524986, 0.0),
        (-1.7833514185499355, 0.9086627233988221, 0.0),
        (-1.9035416074557117, 0.6184979471652929, 0.0),
        (-1.976860256805482, 0.3131036367333192, 0.0),
        (-2.0015020180350076, 0.0, 0.0),
        (-1.976860256805482, -0.3131036367333192, 0.0),
        (-1.9035416074557117, -0.6184979471652929, 0.0),
        (-1.7833514185499355, -0.9086627233988221, 0.0),
        (-1.6192491351309795, -1.176453071524986, 0.0),
        (-1.4152756457581444, -1.4152752878617791, 0.0),
        (-1.1764533101225625, -1.619248777234614, 0.0),
        (-0.908662961996399, -1.7833509413547823, 0.0),
        (-0.6184981261134754, -1.903541130260558, 0.0),
        (-0.31310393498029004, -1.9768597796103284, 0.0),
        (0.0, -2.001501540839854, 0.0),
        (0.3131038455061988, -1.9768597796103284, 0.0),
        (0.6184980068146871, -1.903541130260558, 0.0),
        (0.9086627233988221, -1.7833509413547823, 0.0),
        (1.176453071524986, -1.619248777234614, 0.0),
        (1.4152752878617791, -1.4152752878617791, 0.0),
        (1.619248777234614, -1.176453071524986, 0.0),
        (1.7833509413547823, -0.9086627233988221, 0.0),
        (1.903541130260558, -0.6184979471652929, 0.0),
        (1.9768597796103284, -0.3131036367333192, 0.0),
        (2.001501540839854, 0.0, 0.0),
        (1.9768597796103284, 0.3131036367333192, 0.0),
        (1.903541130260558, 0.6184979471652929, 0.0),
        (1.7833509413547823, 0.9086627233988221, 0.0),
        (1.619248777234614, 1.176453071524986, 0.0),
        (1.4152752878617791, 1.4152752878617791, 0.0),
        (1.176453071524986, 1.619248777234614, 0.0),
        (0.9086627233988221, 1.7833509413547823, 0.0),
        (0.6184980068146871, 1.903541130260558, 0.0),
        (0.3131038455061988, 1.9768597796103284, 0.0),
        (0.0, 2.001501540839854, 0.0),
        (0.0, 1.9768597796103284, -0.31310399462968425),
        (0.0, 1.903541130260558, -0.6184983050616579),
        (0.0, 1.7833509413547823, -0.9086631409445814),
        (0.0, 1.619248777234614, -1.1764536680189277),
        (0.0, 1.4152752878617791, -1.4152760036545093),
        (0.0, 1.176453071524986, -1.6192494930273444),
        (0.0, 0.9086627233988221, -1.7833517764463007),
        (0.0, 0.6184979471652929, -1.903542084650865),
        (0.0, 0.3131036367333192, -1.9768607340006352),
        (0.0, 0.0, -2.001502495230161),
        (0.6184983050616579, 0.0, -1.903542084650865),
        (1.176453787317716, 0.0, -1.619249731624921),
        (1.6192498509237094, 0.0, -1.176453787317716),
        (1.9035423232484419, 0.0, -0.6184983647110521),
        (2.001501540839854, 0.0, 0.0),
        (1.903541130260558, 0.0, 0.6184980068146871),
        (1.619248777234614, 0.0, 1.1764531908237743),
        (1.176453071524986, 0.0, 1.6192488965334026),
        (0.6184979471652929, 0.0, 1.9035412495593464),
        (-5.964939417957824e-08, 0.0, 2.001501779437431),
        (-0.6184981261134754, 0.0, 1.9035413688581349),
        (-1.1764533101225625, 0.0, 1.619249015832191),
        (-1.6192491351309795, 0.0, 1.1764533101225625),
        (-1.9035416074557117, 0.0, 0.6184981261134754),
        (-2.0015020180350076, 0.0, 0.0),
        (-1.9035416074557117, 0.0, -0.6184981261134754),
        (-1.6192492544297676, 0.0, -1.176453429421351),
        (-1.1764535487201393, 0.0, -1.619249373728556),
        (-0.6184983050616579, 0.0, -1.9035419653520766),
        (0.0, 0.0, -2.001502495230161)
    ]
    cvTuples['Half Sphere'] = [
        (-5.964939417957824e-08, 0.0, 2.001501779437431),
        (0.6184979471652929, 0.0, 1.9035412495593464),
        (1.176453071524986, 0.0, 1.6192488965334026),
        (1.619248777234614, 0.0, 1.1764531908237743),
        (1.903541130260558, 0.0, 0.6184980068146871),
        (2.001501540839854, 0.0, 0.0),
        (1.9035423232484419, 0.0, -0.6184983647110521),
        (1.6192498509237094, 0.0, -1.176453787317716),
        (1.176453787317716, 0.0, -1.619249731624921),
        (0.6184983050616579, 0.0, -1.903542084650865),
        (0.0, 0.0, -2.001502495230161),
        (-0.6184983050616579, 0.0, -1.9035419653520766),
        (-1.1764535487201393, 0.0, -1.619249373728556),
        (-1.6192492544297676, 0.0, -1.176453429421351),
        (-1.9035416074557117, 0.0, -0.6184981261134754),
        (-2.0015020180350076, 0.0, 0.0),
        (-1.9035416074557117, 0.0, 0.6184981261134754),
        (-1.6192491351309795, 0.0, 1.1764533101225625),
        (-1.1764533101225625, 0.0, 1.619249015832191),
        (-0.6184981261134754, 0.0, 1.9035413688581349),
        (-5.964939417957824e-08, 0.0, 2.001501779437431),
        (-5.891501246721531e-08, 0.3131036367333192, 1.9768600182079052),
        (-5.672994644226307e-08, 0.6184979471652929, 1.9035413688581349),
        (-5.314799968465514e-08, 0.9086627233988221, 1.7833511799523587),
        (-4.82573740850274e-08, 1.176453071524986, 1.619249015832191),
        (-4.217849039619503e-08, 1.4152752878617791, 1.4152754071605675),
        (-3.5061033711582e-08, 1.619248777234614, 1.1764531908237743),
        (-2.708025942441291e-08, 1.7833509413547823, 0.9086628426976106),
        (-1.843267699523828e-08, 1.903541130260558, 0.6184980664640812),
        (-9.331221744602883e-09, 1.9768597796103284, 0.3131038753308959),
        (0.0, 2.001501540839854, 0.0),
        (0.0, 1.9768597796103284, -0.31310399462968425),
        (0.0, 1.903541130260558, -0.6184983050616579),
        (0.0, 1.7833509413547823, -0.9086631409445814),
        (0.0, 1.619248777234614, -1.1764536680189277),
        (0.0, 1.4152752878617791, -1.4152760036545093),
        (0.0, 1.176453071524986, -1.6192494930273444),
        (0.0, 0.9086627233988221, -1.7833517764463007),
        (0.0, 0.6184979471652929, -1.903542084650865),
        (0.0, 0.3131036367333192, -1.9768607340006352),
        (0.0, 0.0, -2.001502495230161),
        (-0.6184983050616579, 0.0, -1.9035419653520766),
        (-1.1764535487201393, 0.0, -1.619249373728556),
        (-1.6192492544297676, 0.0, -1.176453429421351),
        (-1.9035416074557117, 0.0, -0.6184981261134754),
        (-2.0015020180350076, 0.0, 0.0),
        (-1.976860256805482, 0.3131036367333192, 0.0),
        (-1.9035416074557117, 0.6184979471652929, 0.0),
        (-1.7833514185499355, 0.9086627233988221, 0.0),
        (-1.6192491351309795, 1.176453071524986, 0.0),
        (-1.4152756457581444, 1.4152752878617791, 0.0),
        (-1.1764533101225625, 1.619248777234614, 0.0),
        (-0.908662961996399, 1.7833509413547823, 0.0),
        (-0.6184981261134754, 1.903541130260558, 0.0),
        (-0.31310393498029004, 1.9768597796103284, 0.0),
        (0.0, 2.001501540839854, 0.0),
        (0.3131038455061988, 1.9768597796103284, 0.0),
        (0.6184980068146871, 1.903541130260558, 0.0),
        (0.9086627233988221, 1.7833509413547823, 0.0),
        (1.176453071524986, 1.619248777234614, 0.0),
        (1.4152752878617791, 1.4152752878617791, 0.0),
        (1.619248777234614, 1.176453071524986, 0.0),
        (1.7833509413547823, 0.9086627233988221, 0.0),
        (1.903541130260558, 0.6184979471652929, 0.0),
        (1.9768597796103284, 0.3131036367333192, 0.0),
        (2.001501540839854, 0.0, 0.0)
    ]
    cvTuples['Box'] = [
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, -2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, -2.001501540839854)
    ]
    cvTuples['Pyramid'] = [
        (0.0, 2.490540839504063, 0.0),
        (-1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906),
        (-1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (0.0, 2.490540839504063, 0.0),
        (1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906),
        (1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (0.0, 2.490540839504063, 0.0),
        (-1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906),
        (-1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906)
    ]
    cvTuples['Diamond'] = [
        (0.0, -2.490540839504063, -3.05003297768552e-16),
        (-1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906),
        (0.0, 2.490540839504063, 0.0),
        (1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (0.0, -2.490540839504063, -3.05003297768552e-16),
        (1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906),
        (0.0, 2.490540839504063, 0.0),
        (-1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (1.6603603287505906, -2.033354952212225e-16, 1.6603603287505906),
        (1.6603603287505906, 2.033354952212225e-16, -1.6603603287505906),
        (-1.6603603287505906, 0.0, -1.6603603287505906),
        (-1.6603603287505906, 0.0, 1.6603603287505906),
        (0.0, -2.490540839504063, -3.05003297768552e-16)
    ]
    cvTuples['Circle Pin'] = [
        (0.0, 3.6012403205778734, 0.0),
        (-0.18778610161340414, 3.616019375585509, 0.0),
        (-0.3709482346983487, 3.659992707756567, 0.0),
        (-0.5449764638842179, 3.7320775476619334, 0.0),
        (-0.7055854499305741, 3.830498877526053, 0.0),
        (-0.8488206839113831, 3.952833291509765, 0.0),
        (-0.9711550978950942, 4.096068453940357, 0.0),
        (-1.069576499309432, 4.256677439986713, 0.0),
        (-1.1416613392147976, 4.430705633397475, 0.0),
        (-1.1856346713858557, 4.613867838032635, 0.0),
        (-1.2004137263934913, 4.801653760770498, 0.0),
        (-1.1856346713858557, 4.989439683508361, 0.0),
        (-1.1416613392147976, 5.172601888143522, 0.0),
        (-1.069576499309432, 5.3466300815542835, 0.0),
        (-0.9711550978950942, 5.507239067600639, 0.0),
        (-0.8488206839113831, 5.650474230031231, 0.0),
        (-0.7055854499305741, 5.772808644014942, 0.0),
        (-0.5449764638842179, 5.871229973879063, 0.0),
        (-0.3709482346983487, 5.943314813784429, 0.0),
        (-0.18778610161340414, 5.987288145955486, 0.0),
        (0.0, 6.002067200963123, 0.0),
        (0.1877860479507416, 5.987288145955486, 0.0),
        (0.370948163148132, 5.943314813784429, 0.0),
        (0.5449763207837844, 5.871229973879063, 0.0),
        (0.7055853068301408, 5.772808644014942, 0.0),
        (0.8488204692607332, 5.650474230031231, 0.0),
        (0.9711548832444443, 5.507239067600639, 0.0),
        (1.069576213108565, 5.3466300815542835, 0.0),
        (1.141661053013931, 5.172601888143522, 0.0),
        (1.1856343851849889, 4.989439683508361, 0.0),
        (1.2004134401926245, 4.801653760770498, 0.0),
        (1.1856343851849889, 4.613867838032635, 0.0),
        (1.141661053013931, 4.430705633397475, 0.0),
        (1.069576213108565, 4.256677439986713, 0.0),
        (0.9711548832444443, 4.096068453940357, 0.0),
        (0.8488204692607332, 3.952833291509765, 0.0),
        (0.7055853068301408, 3.830498877526053, 0.0),
        (0.5449763207837844, 3.7320775476619334, 0.0),
        (0.370948163148132, 3.659992707756567, 0.0),
        (0.1877860479507416, 3.616019375585509, 0.0),
        (0.0, 3.6012403205778734, 0.0),
        (0.0, 0.0, 0.0)
    ]
    cvTuples['Square Pin'] = [
        (0.0, 3.602702773511737, 0.0),
        (1.2009009245039124, 3.602702773511737, 0.0),
        (1.2009009245039124, 6.004504622519563, 0.0),
        (-1.2009009245039124, 6.004504622519563, 0.0),
        (-1.2009009245039124, 3.602702773511737, 0.0),
        (0.0, 3.602702773511737, 0.0),
        (0.0, 0.0, 0.0)
    ]
    cvTuples['Sphere Pin'] = [
        (0.0, 0.0, 0.0),
        (0.0, 3.602702773511737, 0.0),
        (0.18786230730371928, 3.6174878302494524, 0.0),
        (0.3710988040888123, 3.661479019859315, 0.0),
        (0.5451976340392933, 3.733593133202781, 0.0),
        (0.7058718429149915, 3.8320544316748815, 0.0),
        (0.8491651727170676, 3.9544385252985825, 0.0),
        (0.9715492663407685, 4.097731855100658, 0.0),
        (1.0700105648128693, 4.258406063976356, 0.0),
        (1.1421246781563348, 4.432504929716473, 0.0),
        (1.1861158677661972, 4.615741515975658, 0.0),
        (1.2009009245039124, 4.80360369801565, 0.0),
        (1.1861158677661972, 4.991465880055642, 0.0),
        (1.1421246781563348, 5.174702466314826, 0.0),
        (1.0700105648128693, 5.3488013320549435, 0.0),
        (0.9715492663407685, 5.509475540930642, 0.0),
        (0.8491651727170676, 5.652768870732717, 0.0),
        (0.7058718429149915, 5.775152964356418, 0.0),
        (0.5451976340392933, 5.873614262828519, 0.0),
        (0.3710988040888123, 5.945728376171985, 0.0),
        (0.18786230730371928, 5.989719565781847, 0.0),
        (0.0, 6.004504622519563, 0.0),
        (-0.18786236098817405, 5.989719565781847, 0.0),
        (-0.3710988756680853, 5.945728376171985, 0.0),
        (-0.5451977771978394, 5.873614262828519, 0.0),
        (-0.7058719860735376, 5.775152964356418, 0.0),
        (-0.8491653874548866, 5.652768870732717, 0.0),
        (-0.9715494810785876, 5.509475540930642, 0.0),
        (-1.070010851129961, 5.3488013320549435, 0.0),
        (-1.142124964473427, 5.174702466314826, 0.0),
        (-1.1861161540832894, 4.991465880055642, 0.0),
        (-1.2009012108210046, 4.80360369801565, 0.0),
        (-1.1861161540832894, 4.615741515975658, 0.0),
        (-1.142124964473427, 4.432504929716473, 0.0),
        (-1.070010851129961, 4.258406063976356, 0.0),
        (-0.9715494810785876, 4.097731855100658, 0.0),
        (-0.8491653874548866, 3.9544385252985825, 0.0),
        (-0.7058719860735376, 3.8320544316748815, 0.0),
        (-0.5451977771978394, 3.733593133202781, 0.0),
        (-0.3710988756680853, 3.661479019859315, 0.0),
        (-0.18786236098817405, 3.6174878302494524, 0.0),
        (0.0, 3.602702773511737, 0.0),
        (0.0, 3.6174878302494524, -0.18786239677781055),
        (0.0, 3.661479019859315, -0.3710989830369948),
        (0.0, 3.733593133202781, -0.5451978845667489),
        (0.0, 3.8320544316748815, -0.7058722008113566),
        (0.0, 3.9544385252985825, -0.8491656021927054),
        (0.0, 4.097731855100658, -0.9715496958164066),
        (0.0, 4.258406063976356, -1.0700110658677802),
        (0.0, 4.432504929716473, -1.142125250790519),
        (0.0, 4.615741515975658, -1.1861164404003812),
        (0.0, 4.80360369801565, -1.2009014971380967),
        (0.0, 4.991465880055642, -1.1861164404003812),
        (0.0, 5.174702466314826, -1.142125250790519),
        (0.0, 5.3488013320549435, -1.0700110658677802),
        (0.0, 5.509475540930642, -0.9715496958164066),
        (0.0, 5.652768870732717, -0.8491656021927054),
        (0.0, 5.775152964356418, -0.7058722008113566),
        (0.0, 5.873614262828519, -0.5451978845667489),
        (0.0, 5.945728376171985, -0.3710989830369948),
        (0.0, 5.989719565781847, -0.18786239677781055),
        (0.0, 6.004504622519563, 0.0),
        (-5.59873304676173e-09, 5.989719565781847, 0.18786232519853754),
        (-1.1059606197142967e-08, 5.945728376171985, 0.37109883987844877),
        (-1.6248155654647748e-08, 5.873614262828519, 0.5451977056185664),
        (-2.10366202269492e-08, 5.775152964356418, 0.7058719144942645),
        (-2.530709423771702e-08, 5.652768870732717, 0.8491652442963404),
        (-2.8954424451016442e-08, 5.509475540930642, 0.9715494094993145),
        (-3.188879981079308e-08, 5.3488013320549435, 1.0700107079714152),
        (-3.403796786535784e-08, 5.174702466314826, 1.142124821314881),
        (-3.534900748032919e-08, 4.991465880055642, 1.186116010924743),
        (-3.5789636507746947e-08, 4.80360369801565, 1.2009010676624585),
        (-3.534900748032919e-08, 4.615741515975658, 1.186116010924743),
        (-3.403796786535784e-08, 4.432504929716473, 1.142124821314881),
        (-3.188879981079308e-08, 4.258406063976356, 1.0700107079714152),
        (-2.8954424451016442e-08, 4.097731855100658, 0.9715494094993145),
        (-2.530709423771702e-08, 3.9544385252985825, 0.8491652442963404),
        (-2.10366202269492e-08, 3.8320544316748815, 0.7058719144942645),
        (-1.6248155654647748e-08, 3.733593133202781, 0.5451977056185664),
        (-1.1059606197142967e-08, 3.661479019859315, 0.37109883987844877),
        (-5.59873304676173e-09, 3.6174878302494524, 0.18786232519853754),
        (0.0, 3.602702773511737, 0.0),
        (0.18786230730371928, 3.6174878302494524, 0.0),
        (0.3710988040888123, 3.661479019859315, 0.0),
        (0.5451976340392933, 3.733593133202781, 0.0),
        (0.7058718429149915, 3.8320544316748815, 0.0),
        (0.8491651727170676, 3.9544385252985825, 0.0),
        (0.9715492663407685, 4.097731855100658, 0.0),
        (1.0700105648128693, 4.258406063976356, 0.0),
        (1.1421246781563348, 4.432504929716473, 0.0),
        (1.1861158677661972, 4.615741515975658, 0.0),
        (1.2009009245039124, 4.80360369801565, 0.0),
        (1.1421246781563348, 4.80360369801565, 0.3710988040888123),
        (0.9715492663407685, 4.80360369801565, 0.7058719144942645),
        (0.7058718429149915, 4.80360369801565, 0.9715493379200414),
        (0.37109876829917576, 4.80360369801565, 1.142124749735608),
        (-3.5789636507746947e-08, 4.80360369801565, 1.2009010676624585),
        (-0.3710988756680853, 4.80360369801565, 1.142124821314881),
        (-0.7058719860735376, 4.80360369801565, 0.9715494094993145),
        (-0.9715494810785876, 4.80360369801565, 0.7058719860735376),
        (-1.142124964473427, 4.80360369801565, 0.3710988756680853),
        (-1.2009012108210046, 4.80360369801565, 0.0),
        (-1.142124964473427, 4.80360369801565, -0.3710988756680853),
        (-0.9715495526578605, 4.80360369801565, -0.7058720576528106),
        (-0.7058721292320835, 4.80360369801565, -0.9715496242371335),
        (-0.3710989830369948, 4.80360369801565, -1.142125179211246),
        (0.0, 4.80360369801565, -1.2009014971380967),
        (0.3710989830369948, 4.80360369801565, -1.142125250790519),
        (0.7058722723906297, 4.80360369801565, -0.9715498389749526),
        (0.9715499105542255, 4.80360369801565, -0.7058722723906297),
        (1.142125393949065, 4.80360369801565, -0.3710990188266313),
        (1.2009009245039124, 4.80360369801565, 0.0)
    ]
    cvTuples['Circle Dumbbell'] = [
        (0.0, 2.105670141066572, 0.0),
        (-0.18722201579424713, 2.120404734416812, 0.0),
        (-0.3698339685099314, 2.164246084748495, 0.0),
        (-0.5433394719014477, 2.2361142994293948, 0.0),
        (-0.7034660038995466, 2.334240177428145, 0.0),
        (-0.8462709483218378, 2.4562069638901654, 0.0),
        (-0.968237913732041, 2.5990119083124563, 0.0),
        (-1.066363672432003, 2.7591385596093443, 0.0),
        (-1.138232006411691, 2.9326438542279805, 0.0),
        (-1.1820732374445857, 3.115255941154802, 0.0),
        (-1.1968078307948251, 3.3024777332638204, 0.0),
        (-1.1820732374445857, 3.4896995253728393, 0.0),
        (-1.138232006411691, 3.672311612299661, 0.0),
        (-1.066363672432003, 3.8458169069182975, 0.0),
        (-0.968237913732041, 4.0059435582151846, 0.0),
        (-0.8462709483218378, 4.148748502637476, 0.0),
        (-0.7034660038995466, 4.270715289099497, 0.0),
        (-0.5433394719014477, 4.368840928500671, 0.0),
        (-0.3698339685099314, 4.440709381779147, 0.0),
        (-0.18722201579424713, 4.48455073211083, 0.0),
        (0.0, 4.499285086863493, 0.0),
        (0.1872219710572015, 4.48455073211083, 0.0),
        (0.3698339088605372, 4.440709381779147, 0.0),
        (0.543339292953265, 4.368840928500671, 0.0),
        (0.7034658249513641, 4.270715289099497, 0.0),
        (0.8462707693736554, 4.148748502637476, 0.0),
        (0.9682376751344642, 4.0059435582151846, 0.0),
        (1.066363433834426, 3.8458169069182975, 0.0),
        (1.1382316485153259, 3.672311612299661, 0.0),
        (1.1820728795482207, 3.4896995253728393, 0.0),
        (1.1968075921972485, 3.3024777332638204, 0.0),
        (1.1820728795482207, 3.115255941154802, 0.0),
        (1.1382316485153259, 2.9326438542279805, 0.0),
        (1.066363433834426, 2.7591385596093443, 0.0),
        (0.9682376751344642, 2.5990119083124563, 0.0),
        (0.8462707693736554, 2.4562069638901654, 0.0),
        (0.7034658249513641, 2.334240177428145, 0.0),
        (0.543339292953265, 2.2361142994293948, 0.0),
        (0.3698339088605372, 2.164246084748495, 0.0),
        (0.1872219710572015, 2.120404734416812, 0.0),
        (0.0, 2.105670141066572, 0.0),
        (0.0, -2.105670141066572, 0.0),
        (0.1872219710572015, -2.120404734416812, 0.0),
        (0.3698339088605372, -2.164246084748495, 0.0),
        (0.543339292953265, -2.2361142994293948, 0.0),
        (0.7034658249513641, -2.334240177428145, 0.0),
        (0.8462707693736554, -2.4562069638901654, 0.0),
        (0.9682376751344642, -2.5990119083124563, 0.0),
        (1.066363433834426, -2.7591385596093443, 0.0),
        (1.1382316485153259, -2.9326438542279805, 0.0),
        (1.1820728795482207, -3.115255941154802, 0.0),
        (1.1968075921972485, -3.3024777332638204, 0.0),
        (1.1820728795482207, -3.4896995253728393, 0.0),
        (1.1382316485153259, -3.672311612299661, 0.0),
        (1.066363433834426, -3.8458169069182975, 0.0),
        (0.9682376751344642, -4.0059435582151846, 0.0),
        (0.8462707693736554, -4.148748502637476, 0.0),
        (0.7034658249513641, -4.270715289099497, 0.0),
        (0.543339292953265, -4.368840928500671, 0.0),
        (0.3698339088605372, -4.440709381779147, 0.0),
        (0.1872219710572015, -4.48455073211083, 0.0),
        (0.0, -4.499285086863493, 0.0),
        (-0.18722201579424713, -4.48455073211083, 0.0),
        (-0.3698339685099314, -4.440709381779147, 0.0),
        (-0.5433394719014477, -4.368840928500671, 0.0),
        (-0.7034660038995466, -4.270715289099497, 0.0),
        (-0.8462709483218378, -4.148748502637476, 0.0),
        (-0.968237913732041, -4.0059435582151846, 0.0),
        (-1.066363672432003, -3.8458169069182975, 0.0),
        (-1.138232006411691, -3.672311612299661, 0.0),
        (-1.1820732374445857, -3.4896995253728393, 0.0),
        (-1.1968078307948251, -3.3024777332638204, 0.0),
        (-1.1820732374445857, -3.115255941154802, 0.0),
        (-1.138232006411691, -2.9326438542279805, 0.0),
        (-1.066363672432003, -2.7591385596093443, 0.0),
        (-0.968237913732041, -2.5990119083124563, 0.0),
        (-0.8462709483218378, -2.4562069638901654, 0.0),
        (-0.7034660038995466, -2.334240177428145, 0.0),
        (-0.5433394719014477, -2.2361142994293948, 0.0),
        (-0.3698339685099314, -2.164246084748495, 0.0),
        (-0.18722201579424713, -2.120404734416812, 0.0),
        (0.0, -2.105670141066572, 0.0)
    ]
    cvTuples['Square Dumbbell'] = [
        (0.0, 2.1015767610403926, 0.0),
        (-1.2009009722234278, 2.1015767610403926, 0.0),
        (-1.2009009722234278, 4.5033784668896715, 0.0),
        (1.2009009722234278, 4.5033784668896715, 0.0),
        (1.2009009722234278, 2.1015767610403926, 0.0),
        (0.0, 2.1015767610403926, 0.0),
        (0.0, -2.1015767610403926, 0.0),
        (1.2009009722234278, -2.1015767610403926, 0.0),
        (1.2009009722234278, -4.5033784668896715, 0.0),
        (-1.2009009722234278, -4.5033784668896715, 0.0),
        (-1.2009009722234278, -2.1015767610403926, 0.0),
        (0.0, -2.1015767610403926, 0.0)
    ]
    cvTuples['Sphere Dumbbell'] = [
        (0.0, 2.105579712584996, 0.0),
        (-0.1872361527006677, 2.120315498923119, 0.0),
        (-0.36986188442640744, 2.164160189620876, 0.0),
        (-0.543380451035249, 2.2360338920460405, 0.0),
        (-0.7035190918603664, 2.3341669279720922, 0.0),
        (-0.8463348328230041, 2.4561430197396046, 0.0),
        (-0.9683109842399111, 2.5989589396504256, 0.0),
        (-1.066444079815357, 2.7590975208261486, 0.0),
        (-1.1383179015393095, 2.932616176909081, 0.0),
        (-1.1821624729382783, 3.1152416253001984, 0.0),
        (-1.196898139977613, 3.3024777332638204, 0.0),
        (-1.1383179015393095, 3.3024777332638204, -0.36986188442640744),
        (-0.9683110438893051, 3.3024777332638204, -0.7035191515097606),
        (-0.7035192111591547, 3.3024777332638204, -0.9683111035386994),
        (-0.36986197390049874, 3.3024777332638204, -1.1383180208380979),
        (0.0, 3.3024777332638204, -1.196898497873978),
        (0.36986197390049874, 3.3024777332638204, -1.1383181401368863),
        (0.7035193304579431, 3.3024777332638204, -0.9683113421362762),
        (0.9683114017856704, 3.3024777332638204, -0.7035193304579431),
        (1.1383182594356747, 3.3024777332638204, -0.36986200372519584),
        (1.1968979013800363, 3.3024777332638204, 0.0),
        (1.1383175436429445, 3.3024777332638204, 0.36986179495231614),
        (0.9683107456423343, 3.3024777332638204, 0.703518972561578),
        (0.7035189129121839, 3.3024777332638204, 0.9683108052917285),
        (0.3698617651276191, 3.3024777332638204, 1.1383176629417329),
        (-3.567033712208379e-08, 3.3024777332638204, 1.1968980206788247),
        (-0.36986188442640744, 3.3024777332638204, 1.1383176629417329),
        (-0.7035190918603664, 3.3024777332638204, 0.9683109245905169),
        (-0.9683109842399111, 3.3024777332638204, 0.7035190918603664),
        (-1.1383179015393095, 3.3024777332638204, 0.36986188442640744),
        (-1.196898139977613, 3.3024777332638204, 0.0),
        (-1.1821624729382783, 3.4897138412274424, 0.0),
        (-1.1383179015393095, 3.6723392896185603, 0.0),
        (-1.066444079815357, 3.8458579457014928, 0.0),
        (-0.9683109842399111, 4.005996526877216, 0.0),
        (-0.8463348328230041, 4.148812446788036, 0.0),
        (-0.7035190918603664, 4.270788299957973, 0.0),
        (-0.543380451035249, 4.368921574481601, 0.0),
        (-0.36986188442640744, 4.440795276906766, 0.0),
        (-0.1872361527006677, 4.484639967604522, 0.0),
        (0.0, 4.499375753942646, 0.0),
        (0.18723609305127353, 4.484639967604522, 0.0),
        (0.36986179495231614, 4.440795276906766, 0.0),
        (0.5433802720870665, 4.368921574481601, 0.0),
        (0.7035189129121839, 4.270788299957973, 0.0),
        (0.8463345942254276, 4.148812446788036, 0.0),
        (0.9683107456423343, 4.005996526877216, 0.0),
        (1.0664438412177804, 3.8458579457014928, 0.0),
        (1.1383175436429445, 3.6723392896185603, 0.0),
        (1.1821621150419133, 3.4897138412274424, 0.0),
        (1.1821621150419133, 3.1152416253001984, 0.0),
        (1.1383175436429445, 2.932616176909081, 0.0),
        (1.0664438412177804, 2.7590975208261486, 0.0),
        (0.9683107456423343, 2.5989589396504256, 0.0),
        (0.8463345942254276, 2.4561430197396046, 0.0),
        (0.7035189129121839, 2.3341669279720922, 0.0),
        (0.5433802720870665, 2.2360338920460405, 0.0),
        (0.36986179495231614, 2.164160189620876, 0.0),
        (0.18723609305127353, 2.120315498923119, 0.0),
        (0.0, 2.105579712584996, 0.0),
        (-5.580070407726572e-09, 2.120315498923119, 0.18723610796362208),
        (-1.1022740452060584e-08, 2.164160189620876, 0.36986182477701324),
        (-1.6193994047852353e-08, 2.2360338920460405, 0.5433803913858548),
        (-2.0966497448449848e-08, 2.3341669279720922, 0.703518972561578),
        (-2.5222736424965488e-08, 2.4561430197396046, 0.8463346538748218),
        (-2.885790901310248e-08, 2.5989589396504256, 0.9683109245905169),
        (-3.178250316434444e-08, 2.7590975208261486, 1.0664439605165685),
        (-3.392450641521646e-08, 2.932616176909081, 1.1383176629417329),
        (-3.523117646699885e-08, 3.1152416253001984, 1.1821622343407017),
        (-3.567033712208379e-08, 3.3024777332638204, 1.1968980206788247),
        (-3.523117646699885e-08, 3.4897138412274424, 1.1821622343407017),
        (-3.392450641521646e-08, 3.6723392896185603, 1.1383176629417329),
        (-3.178250316434444e-08, 3.8458579457014928, 1.0664439605165685),
        (-2.885790901310248e-08, 4.005996526877216, 0.9683109245905169),
        (-2.5222736424965488e-08, 4.148812446788036, 0.8463346538748218),
        (-2.0966497448449848e-08, 4.270788299957973, 0.703518972561578),
        (-1.6193994047852353e-08, 4.368921574481601, 0.5433803913858548),
        (-1.1022740452060584e-08, 4.440795276906766, 0.36986182477701324),
        (-5.580070407726572e-09, 4.484639967604522, 0.18723610796362208),
        (0.0, 4.499375753942646, 0.0),
        (0.0, 4.484639967604522, -0.18723618252536478),
        (0.0, 4.440795276906766, -0.36986197390049874),
        (0.0, 4.368921574481601, -0.5433805703340373),
        (0.0, 4.270788299957973, -0.7035192708085489),
        (0.0, 4.148812446788036, -0.8463350117711868),
        (0.0, 4.005996526877216, -0.9683111631880936),
        (0.0, 3.8458579457014928, -1.0664443184129337),
        (0.0, 3.6723392896185603, -1.1383181401368863),
        (0.0, 3.4897138412274424, -1.182162711535855),
        (0.0, 3.3024777332638204, -1.196898497873978),
        (0.0, 3.1152416253001984, -1.182162711535855),
        (0.0, 2.932616176909081, -1.1383181401368863),
        (0.0, 2.7590975208261486, -1.0664443184129337),
        (0.0, 2.5989589396504256, -0.9683111631880936),
        (0.0, 2.4561430197396046, -0.8463350117711868),
        (0.0, 2.3341669279720922, -0.7035192708085489),
        (0.0, 2.2360338920460405, -0.5433805703340373),
        (0.0, 2.164160189620876, -0.36986197390049874),
        (0.0, 2.120315498923119, -0.18723618252536478),
        (0.0, 2.105579712584996, 0.0),
        (0.0, -2.105670141066572, 0.0),
        (0.0, -2.120404734416812, -0.18722206053129278),
        (0.0, -2.164246084748495, -0.3698340878087198),
        (0.0, -2.2361142994293948, -0.5433395315508418),
        (0.0, -2.334240177428145, -0.7034661828477291),
        (0.0, -2.4562069638901654, -0.8462711869194146),
        (0.0, -2.5990119083124563, -0.9682380926802238),
        (0.0, -2.7591385596093443, -1.0663639110295795),
        (0.0, -2.9326438542279805, -1.1382322450092677),
        (0.0, -3.115255941154802, -1.1820734760421625),
        (0.0, -3.3024777332638204, -1.19680818869119),
        (0.3698340878087198, -3.3024777332638204, -1.1382322450092677),
        (0.7034662424971233, -3.3024777332638204, -0.9682382716284061),
        (0.9682383312778003, -3.3024777332638204, -0.7034662424971233),
        (1.138232364308056, -3.3024777332638204, -0.36983411763341684),
        (1.1968075921972485, -3.3024777332638204, 0.0),
        (1.1382316485153259, -3.3024777332638204, 0.3698339088605372),
        (0.9682376751344642, -3.3024777332638204, 0.7034658846007582),
        (0.7034658249513641, -3.3024777332638204, 0.9682377347838584),
        (0.36983384921114304, -3.3024777332638204, 1.1382317678141143),
        (-3.566764569870378e-08, -3.3024777332638204, 1.1968077114960367),
        (-0.3698339685099314, -3.3024777332638204, 1.1382318871129027),
        (-0.7034660038995466, -3.3024777332638204, 0.9682378540826468),
        (-0.968237913732041, -3.3024777332638204, 0.7034660038995466),
        (-1.138232006411691, -3.3024777332638204, 0.3698339685099314),
        (-1.1968078307948251, -3.3024777332638204, 0.0),
        (-1.138232006411691, -3.3024777332638204, -0.3698339685099314),
        (-0.9682379733814352, -3.3024777332638204, -0.7034660635489408),
        (-0.7034661231983349, -3.3024777332638204, -0.9682380330308296),
        (-0.3698340878087198, -3.3024777332638204, -1.1382322450092677),
        (0.0, -3.3024777332638204, -1.19680818869119),
        (0.0, -3.4896995253728393, -1.1820734760421625),
        (0.0, -3.672311612299661, -1.1382322450092677),
        (0.0, -3.8458169069182975, -1.0663639110295795),
        (0.0, -4.0059435582151846, -0.9682380926802238),
        (0.0, -4.148748502637476, -0.8462711869194146),
        (0.0, -4.270715289099497, -0.7034661828477291),
        (0.0, -4.368840928500671, -0.5433395315508418),
        (0.0, -4.440709381779147, -0.3698340878087198),
        (0.0, -4.48455073211083, -0.18722206053129278),
        (0.0, -4.499285086863493, 0.0),
        (-5.57964953950648e-09, -4.48455073211083, 0.18722198596955006),
        (-1.1021909381763255e-08, -4.440709381779147, 0.3698339386852343),
        (-1.619277277449563e-08, -4.368840928500671, 0.5433393526026593),
        (-2.096491530392659e-08, -4.270715289099497, 0.7034658846007582),
        (-2.5220834296156627e-08, -4.148748502637476, 0.8462708290230496),
        (-2.8855731342269905e-08, -4.0059435582151846, 0.9682378540826468),
        (-3.1780106837583366e-08, -3.8458169069182975, 1.0663635531332145),
        (-3.392194654093164e-08, -3.672311612299661, 1.1382318871129027),
        (-3.52285170420474e-08, -3.4896995253728393, 1.1820731181457973),
        (-3.566764569870378e-08, -3.3024777332638204, 1.1968077114960367),
        (-3.52285170420474e-08, -3.115255941154802, 1.1820731181457973),
        (-3.392194654093164e-08, -2.9326438542279805, 1.1382318871129027),
        (-3.1780106837583366e-08, -2.7591385596093443, 1.0663635531332145),
        (-2.8855731342269905e-08, -2.5990119083124563, 0.9682378540826468),
        (-2.5220834296156627e-08, -2.4562069638901654, 0.8462708290230496),
        (-2.096491530392659e-08, -2.334240177428145, 0.7034658846007582),
        (-1.619277277449563e-08, -2.2361142994293948, 0.5433393526026593),
        (-1.1021909381763255e-08, -2.164246084748495, 0.3698339386852343),
        (-5.57964953950648e-09, -2.120404734416812, 0.18722198596955006),
        (0.0, -2.105670141066572, 0.0),
        (0.1872219710572015, -2.120404734416812, 0.0),
        (0.3698339088605372, -2.164246084748495, 0.0),
        (0.543339292953265, -2.2361142994293948, 0.0),
        (0.7034658249513641, -2.334240177428145, 0.0),
        (0.8462707693736554, -2.4562069638901654, 0.0),
        (0.9682376751344642, -2.5990119083124563, 0.0),
        (1.066363433834426, -2.7591385596093443, 0.0),
        (1.1382316485153259, -2.9326438542279805, 0.0),
        (1.1820728795482207, -3.115255941154802, 0.0),
        (1.1968075921972485, -3.3024777332638204, 0.0),
        (1.1820728795482207, -3.4896995253728393, 0.0),
        (1.1382316485153259, -3.672311612299661, 0.0),
        (1.066363433834426, -3.8458169069182975, 0.0),
        (0.9682376751344642, -4.0059435582151846, 0.0),
        (0.8462707693736554, -4.148748502637476, 0.0),
        (0.7034658249513641, -4.270715289099497, 0.0),
        (0.543339292953265, -4.368840928500671, 0.0),
        (0.3698339088605372, -4.440709381779147, 0.0),
        (0.1872219710572015, -4.48455073211083, 0.0),
        (0.0, -4.499285086863493, 0.0),
        (-0.18722201579424713, -4.48455073211083, 0.0),
        (-0.3698339685099314, -4.440709381779147, 0.0),
        (-0.5433394719014477, -4.368840928500671, 0.0),
        (-0.7034660038995466, -4.270715289099497, 0.0),
        (-0.8462709483218378, -4.148748502637476, 0.0),
        (-0.968237913732041, -4.0059435582151846, 0.0),
        (-1.066363672432003, -3.8458169069182975, 0.0),
        (-1.138232006411691, -3.672311612299661, 0.0),
        (-1.1820732374445857, -3.4896995253728393, 0.0),
        (-1.1968078307948251, -3.3024777332638204, 0.0),
        (-1.1820732374445857, -3.115255941154802, 0.0),
        (-1.138232006411691, -2.9326438542279805, 0.0),
        (-1.066363672432003, -2.7591385596093443, 0.0),
        (-0.968237913732041, -2.5990119083124563, 0.0),
        (-0.8462709483218378, -2.4562069638901654, 0.0),
        (-0.7034660038995466, -2.334240177428145, 0.0),
        (-0.5433394719014477, -2.2361142994293948, 0.0),
        (-0.3698339685099314, -2.164246084748495, 0.0),
        (-0.18722201579424713, -2.120404734416812, 0.0),
        (0.0, -2.105670141066572, 0.0)
    ]
    cvTuples['Cross'] = [
        (-1.000750770419927, 0.0, -2.001501540839854),
        (1.000750770419927, 0.0, -2.001501540839854),
        (1.000750770419927, 0.0, -1.000750770419927),
        (2.001501540839854, 0.0, -1.000750770419927),
        (2.001501540839854, 0.0, 1.000750770419927),
        (1.000750770419927, 0.0, 1.000750770419927),
        (1.000750770419927, 0.0, 2.001501540839854),
        (-1.000750770419927, 0.0, 2.001501540839854),
        (-1.000750770419927, 0.0, 1.000750770419927),
        (-2.001501540839854, 0.0, 1.000750770419927),
        (-2.001501540839854, 0.0, -1.000750770419927),
        (-1.000750770419927, 0.0, -1.000750770419927),
        (-1.000750770419927, 0.0, -2.001501540839854)
    ]
    cvTuples['Cross Thin'] = [
        (-0.40030030816797085, 0.0, -2.001501540839854),
        (-0.40030030816797085, 0.0, -0.40030030816797085),
        (-2.001501540839854, 0.0, -0.40030030816797085),
        (-2.001501540839854, 0.0, 0.40030030816797085),
        (-0.40030030816797085, 0.0, 0.40030030816797085),
        (-0.40030030816797085, 0.0, 2.001501540839854),
        (0.40030030816797085, 0.0, 2.001501540839854),
        (0.40030030816797085, 0.0, 0.40030030816797085),
        (2.001501540839854, 0.0, 0.40030030816797085),
        (2.001501540839854, 0.0, -0.40030030816797085),
        (0.40030030816797085, 0.0, -0.40030030816797085),
        (0.40030030816797085, 0.0, -2.001501540839854),
        (-0.40030030816797085, 0.0, -2.001501540839854)
    ]
    cvTuples['Locator'] = [
        (0.0, 2.001501540839854, 0.0),
        (0.0, -2.001501540839854, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, -2.001501540839854),
        (0.0, 0.0, 2.001501540839854),
        (0.0, 0.0, 0.0),
        (2.001501540839854, 0.0, 0.0),
        (-2.001501540839854, 0.0, 0.0)
    ]
    cvTuples['Four Arrows'] = [
        (0.0, 0.0, -2.001501540839854),
        (0.8006006163359417, 0.0, -1.2009009245039126),
        (0.40030030816797085, 0.0, -1.2009009245039126),
        (0.40030030816797085, 0.0, -0.40030030816797085),
        (1.2009009245039126, 0.0, -0.40030030816797085),
        (1.2009009245039126, 0.0, -0.8006006163359417),
        (2.001501540839854, 0.0, 0.0),
        (1.2009009245039126, 0.0, 0.8006006163359417),
        (1.2009009245039126, 0.0, 0.40030030816797085),
        (0.40030030816797085, 0.0, 0.40030030816797085),
        (0.40030030816797085, 0.0, 1.2009009245039126),
        (0.8006006163359417, 0.0, 1.2009009245039126),
        (0.0, 0.0, 2.001501540839854),
        (-0.8006006163359417, 0.0, 1.2009009245039126),
        (-0.40030030816797085, 0.0, 1.2009009245039126),
        (-0.40030030816797085, 0.0, 0.40030030816797085),
        (-1.2009009245039126, 0.0, 0.40030030816797085),
        (-1.2009009245039126, 0.0, 0.8006006163359417),
        (-2.001501540839854, 0.0, 0.0),
        (-1.2009009245039126, 0.0, -0.8006006163359417),
        (-1.2009009245039126, 0.0, -0.40030030816797085),
        (-0.40030030816797085, 0.0, -0.40030030816797085),
        (-0.40030030816797085, 0.0, -1.2009009245039126),
        (-0.8006006163359417, 0.0, -1.2009009245039126),
        (0.0, 0.0, -2.001501540839854)
    ]
    cvTuples['Four Arrows Thin'] = [
        (0.0, 0.0, -1.9995000392990145),
        (0.6665000130996714, 0.0, -1.3330000261993429),
        (0.16662500327491786, 0.0, -1.3330000261993429),
        (0.16662500327491786, 0.0, -0.16662500327491786),
        (1.3330000261993429, 0.0, -0.16662500327491786),
        (1.3330000261993429, 0.0, -0.6665000130996714),
        (1.9995000392990145, 0.0, 0.0),
        (1.3330000261993429, 0.0, 0.6665000130996714),
        (1.3330000261993429, 0.0, 0.16662500327491786),
        (0.16662500327491786, 0.0, 0.16662500327491786),
        (0.16662500327491786, 0.0, 1.3330000261993429),
        (0.6665000130996714, 0.0, 1.3330000261993429),
        (0.0, 0.0, 1.9995000392990145),
        (-0.6665000130996714, 0.0, 1.3330000261993429),
        (-0.16662500327491786, 0.0, 1.3330000261993429),
        (-0.16662500327491786, 0.0, 0.16662500327491786),
        (-1.3330000261993429, 0.0, 0.16662500327491786),
        (-1.3330000261993429, 0.0, 0.6665000130996714),
        (-1.9995000392990145, 0.0, 0.0),
        (-1.3330000261993429, 0.0, -0.6665000130996714),
        (-1.3330000261993429, 0.0, -0.16662500327491786),
        (-0.16662500327491786, 0.0, -0.16662500327491786),
        (-0.16662500327491786, 0.0, -1.3330000261993429),
        (-0.6665000130996714, 0.0, -1.3330000261993429),
        (0.0, 0.0, -1.9995000392990145)
    ]
    cvTuples['Curved Four Arrows'] = [
        (1.9917258826883961, -0.3993344826837887, 0.0),
        (1.3330000261993429, 0.16673135099852496, 0.8886666841328953),
        (1.3330000261993429, 0.16673134580034765, 0.44433334206644765),
        (0.8886666841328953, 0.33548407942743624, 0.44433334206644765),
        (0.44433334206644765, 0.3993344826837886, 0.44433334206644765),
        (0.44433334206644765, 0.33548407942743624, 0.8886666841328953),
        (0.44433334206644765, 0.16673134580034765, 1.3330000261993429),
        (0.8886666841328953, 0.16673135099852496, 1.3330000261993429),
        (0.0, -0.3993344826837887, 1.9917258826883961),
        (-0.8886666841328953, 0.16673135099852496, 1.3330000261993429),
        (-0.44433334206644765, 0.16673134580034765, 1.3330000261993429),
        (-0.44433334206644765, 0.33548407942743624, 0.8886666841328953),
        (-0.44433334206644765, 0.3993344826837886, 0.44433334206644765),
        (-0.8886666841328953, 0.33548407942743624, 0.44433334206644765),
        (-1.3330000261993429, 0.16673134580034765, 0.44433334206644765),
        (-1.3330000261993429, 0.16673135099852496, 0.8886666841328953),
        (-1.9917258826883961, -0.3993344826837887, 0.0),
        (-1.3330000261993429, 0.16673135099852496, -0.8886666841328953),
        (-1.3330000261993429, 0.16673134580034765, -0.44433334206644765),
        (-0.8886666841328953, 0.33548407942743624, -0.44433334206644765),
        (-0.44433334206644765, 0.3993344826837886, -0.44433334206644765),
        (-0.44433334206644765, 0.33548407942743624, -0.8886666841328953),
        (-0.44433334206644765, 0.16673134580034765, -1.3330000261993429),
        (-0.8886666841328953, 0.16673135099852496, -1.3330000261993429),
        (0.0, -0.3993344826837887, -1.9917258826883961),
        (0.8886666841328953, 0.16673135099852496, -1.3330000261993429),
        (0.44433334206644765, 0.16673134580034765, -1.3330000261993429),
        (0.44433334206644765, 0.33548407942743624, -0.8886666841328953),
        (0.44433334206644765, 0.3993344826837886, -0.44433334206644765),
        (0.8886666841328953, 0.33548407942743624, -0.44433334206644765),
        (1.3330000261993429, 0.16673134580034765, -0.44433334206644765),
        (1.3330000261993429, 0.16673135099852496, -0.8886666841328953),
        (1.9917258826883961, -0.3993344826837887, 0.0)
    ]
    cvTuples['Curved Four Arrows Thin'] = [
        (0.0, -0.5758674561293435, -2.0128282558399926),
        (0.7623196350268492, -0.09125630012069194, -1.5246392700536984),
        (0.1905799087567123, -0.09125630012069194, -1.5246392700536984),
        (0.19264094262533524, 0.19817013157252422, -1.1558456557520116),
        (0.18705145848290533, 0.4539151983439914, -0.7482058339316213),
        (0.18705145848290533, 0.5758674561293435, -0.18705145848290533),
        (0.7482058339316213, 0.4539151983439914, -0.18705145848290533),
        (1.1558456557520116, 0.19817013157252422, -0.19264094262533524),
        (1.5246392700536984, -0.09125630012069194, -0.1905799087567123),
        (1.5246392700536984, -0.09125630012069194, -0.7623196350268492),
        (2.0128282558399926, -0.5758674561293435, 0.0),
        (1.5246392700536984, -0.09125630012069194, 0.7623196350268492),
        (1.5246392700536984, -0.09125630012069194, 0.1905799087567123),
        (1.1558456557520116, 0.19817013157252422, 0.19264094262533524),
        (0.7482058339316213, 0.4539151983439914, 0.18705145848290533),
        (0.18705145848290533, 0.5758674561293435, 0.18705145848290533),
        (0.18705145848290533, 0.4539151983439914, 0.7482058339316213),
        (0.19264094262533524, 0.19817013157252422, 1.1558456557520116),
        (0.1905799087567123, -0.09125630012069194, 1.5246392700536984),
        (0.7623196350268492, -0.09125630012069194, 1.5246392700536984),
        (0.0, -0.5758674561293435, 2.0128282558399926),
        (-0.7623196350268492, -0.09125630012069194, 1.5246392700536984),
        (-0.1905799087567123, -0.09125630012069194, 1.5246392700536984),
        (-0.19264094262533524, 0.19817013157252422, 1.1558456557520116),
        (-0.18705145848290533, 0.4539151983439914, 0.7482058339316213),
        (-0.18705145848290533, 0.5758674561293435, 0.18705145848290533),
        (-0.7482058339316213, 0.4539151983439914, 0.18705145848290533),
        (-1.1558456557520116, 0.19817013157252422, 0.19264094262533524),
        (-1.5246392700536984, -0.09125630012069194, 0.1905799087567123),
        (-1.5246392700536984, -0.09125630012069194, 0.7623196350268492),
        (-2.0128282558399926, -0.5758674561293435, 0.0),
        (-1.5246392700536984, -0.09125630012069194, -0.7623196350268492),
        (-1.5246392700536984, -0.09125630012069194, -0.1905799087567123),
        (-1.1558456557520116, 0.19817013157252422, -0.19264094262533524),
        (-0.7482058339316213, 0.4539151983439914, -0.18705145848290533),
        (-0.18705145848290533, 0.5758674561293435, -0.18705145848290533),
        (-0.18705145848290533, 0.4539151983439914, -0.7482058339316213),
        (-0.19264094262533524, 0.19817013157252422, -1.1558456557520116),
        (-0.1905799087567123, -0.09125630012069194, -1.5246392700536984),
        (-0.7623196350268492, -0.09125630012069194, -1.5246392700536984),
        (0.0, -0.5758674561293435, -2.0128282558399926)
    ]
    cvTuples['Two Arrows'] = [
        (0.0, 0.0, -2.4246948424842265),
        (0.9698779369936905, 0.0, -1.4548169054905358),
        (0.48493896849684526, 0.0, -1.4548169054905358),
        (0.48493896849684526, 0.0, 1.4548169054905358),
        (0.9698779369936905, 0.0, 1.4548169054905358),
        (0.0, 0.0, 2.4246948424842265),
        (-0.9698779369936905, 0.0, 1.4548169054905358),
        (-0.48493896849684526, 0.0, 1.4548169054905358),
        (-0.48493896849684526, 0.0, -1.4548169054905358),
        (-0.9698779369936905, 0.0, -1.4548169054905358),
        (0.0, 0.0, -2.4246948424842265)
    ]
    cvTuples['Two Arrows Thin'] = [
        (0.0, 0.0, -2.4246948424842265),
        (0.9698779369936905, 0.0, -1.4548169054905358),
        (0.25863410610275417, 0.0, -1.4548169054905358),
        (0.25863410610275417, 0.0, 1.4548169054905358),
        (0.9698779369936905, 0.0, 1.4548169054905358),
        (0.0, 0.0, 2.4246948424842265),
        (-0.9698779369936905, 0.0, 1.4548169054905358),
        (-0.25863410610275417, 0.0, 1.4548169054905358),
        (-0.25863410610275417, 0.0, -1.4548169054905358),
        (-0.9698779369936905, 0.0, -1.4548169054905358),
        (0.0, 0.0, -2.4246948424842265)
    ]
    cvTuples['Curved Two Arrows'] = [
        (0.0, -1.110514931482559, -2.4255007827347024),
        (0.0, 0.7726167603219469, -2.2923655188962426),
        (0.0, -0.14948435475560623, -2.088726321246109),
        (0.0, 0.37916795728442704, -1.765270473803264),
        (0.0, 0.9203469777352036, -0.9554496328243811),
        (0.0, 1.1105149314825558, 0.0),
        (0.0, 0.9203469777352036, 0.9554496328243811),
        (0.0, 0.37916795728442704, 1.7652704738032645),
        (0.0, -0.1453987410465091, 2.093099498453956),
        (0.0, 0.7726167603219469, 2.2923655188962426),
        (0.0, -1.110514931482559, 2.4255007827347024),
        (0.0, -0.19669122111505885, 0.7735812040562016),
        (0.0, -0.4111184740219825, 1.7445349335167957),
        (0.0, 0.05782017149007778, 1.4444491504143115),
        (0.0, 0.5012099061520471, 0.7816374060749043),
        (0.0, 0.6563725339944193, 0.0),
        (0.0, 0.5012099061520471, -0.7816374060749043),
        (0.0, 0.05782017149007778, -1.4444491504143115),
        (0.0, -0.4146179005990214, -1.7377263146772652),
        (0.0, -0.19669122111505885, -0.7735812040562015),
        (0.0, -1.110514931482559, -2.4255007827347024)
    ]
    cvTuples['Curved Two Arrows Thin'] = [
        (0.0, -0.9694380161318109, -2.4255004686919825),
        (0.0, 0.2502008909280916, -2.339273865903459),
        (0.0, -0.4071169757601066, -2.2217294706311543),
        (0.0, -0.20609428352032405, -2.1166205025664993),
        (0.0, 0.16907930798787674, -1.850113633834823),
        (0.0, 0.60231593394469, -1.3148291415184596),
        (0.0, 0.8759478631194588, -0.6825492720843684),
        (0.0, 0.9694380161318039, 2.3418263709112653e-08),
        (0.0, 0.8759478631194588, 0.6825492720843684),
        (0.0, 0.60231593394469, 1.3148291415184596),
        (0.0, 0.16907930798787674, 1.850113633834823),
        (0.0, -0.20609428352032405, 2.1166205025664993),
        (0.0, -0.4071169757601066, 2.2217294706311543),
        (0.0, 0.2502008909280916, 2.3392738659034586),
        (0.0, -0.9694380161318109, 2.4255004686919825),
        (0.0, -0.37758522389678706, 1.3556096064338674),
        (0.0, -0.5177774738281845, 2.0101481264881023),
        (0.0, -0.33594277948406914, 1.915060565487676),
        (0.0, 0.0036508771506296744, 1.67384957153285),
        (0.0, 0.3954766709142305, 1.1896558695317854),
        (0.0, 0.643141766202062, 0.6175187690121082),
        (0.0, 0.7276635120347005, 2.1187647032259625e-08),
        (0.0, 0.643141766202062, -0.6175187690121082),
        (0.0, 0.3954766709142305, -1.1896558695317854),
        (0.0, 0.0036508771506296744, -1.6738495715328499),
        (0.0, -0.33594277948406914, -1.9150605654876764),
        (0.0, -0.5177774738281845, -2.010148126488103),
        (0.0, -0.37758522389678706, -1.3556096064338676),
        (0.0, -0.9694380161318109, -2.4255004686919825)
    ]
    cvTuples['One Arrow'] = [
        (0.0, 0.0, -2.001501540839854),
        (1.6012012326718834, 0.0, -0.40030030816797085),
        (0.8006006163359417, 0.0, -0.40030030816797085),
        (0.8006006163359417, 0.0, 2.001501540839854),
        (-0.8006006163359417, 0.0, 2.001501540839854),
        (-0.8006006163359417, 0.0, -0.40030030816797085),
        (-1.6012012326718834, 0.0, -0.40030030816797085),
        (0.0, 0.0, -2.001501540839854)
    ]
    cvTuples['One Arrow Thin'] = [
        (0.0, 0.0, -2.0),
        (1.2987239525074818, 0.0, -0.40030030816797085),
        (0.40030030816797085, 0.0, -0.40030030816797085),
        (0.40030030816797085, 0.0, 2.001501540839854),
        (-0.40030030816797085, 0.0, 2.001501540839854),
        (-0.40030030816797085, 0.0, -0.40030030816797085),
        (-1.2987239525074818, 0.0, -0.40030030816797085),
        (0.0, 0.0, -2.0)
    ]
    cvTuples['Circle One Arrow'] = [
        (1.099320267429756, -1.6524720822501887e-18, -0.35719078779323343),
        (1.1558929681777954, 0.0, 0.0),
        (1.099319577217102, 0.0, 0.3571905791759491),
        (0.9351370930671692, 0.0, 0.6794168949127197),
        (0.679416835308075, 0.0, 0.935137152671814),
        (0.3571905493736267, 0.0, 1.099319577217102),
        (-3.44482948833047e-08, 0.0, 1.1558930873870852),
        (-0.35719063878059387, 0.0, 1.0993196964263916),
        (-0.6794169545173645, 0.0, 0.9351372122764587),
        (-0.9351372718811035, 0.0, 0.6794169545173645),
        (-1.0993198156356812, 0.0, 0.35719063878059387),
        (-1.1558932065963745, 0.0, 0.0),
        (-1.0993198156356812, 0.0, -0.35719063878059387),
        (-0.9351373314857483, 0.0, -0.6794170141220093),
        (-0.6794171333312988, 0.0, -0.9351373910903931),
        (-0.3571907579898834, 0.0, -1.0993200540542603),
        (-0.3571907579898834, 8.312129504056783e-17, -1.3590328031514498),
        (-0.6794171333312988, 1.747100930194013e-16, -1.3590327642548976),
        (0.0, 0.0, -1.9947055969799072),
        (0.6794172525405884, -1.7092196482691121e-16, -1.3590328143179529),
        (0.3571907579898834, -7.852078120989922e-17, -1.3599486032411954),
        (0.35719075798988337, 0.0, -1.0993201732635498),
        (0.6794172525405884, 0.0, -0.9351376295089722),
        (0.9351376891136169, 0.0, -0.6794172525405884),
        (1.0993203175159225, 1.6524720822501887e-18, -0.35719078779117824)
    ]
    cvTuples['Circle Two Arrows'] = [
        (0.9351376625974113, 0.0, -0.6794173552984247),
        (1.0993202924728394, 0.0, -0.3571907877922058),
        (1.1558929681777954, 0.0, 0.0),
        (1.099319577217102, 0.0, 0.3571905791759491),
        (0.9351370930671692, 0.0, 0.6794168949127197),
        (0.679416835308075, 0.0, 0.9351371526718141),
        (0.3571905493736267, 0.0, 1.099319577217102),
        (0.3571905493736267, -9.431608323763676e-17, 1.322568297385874),
        (0.679417252539371, -1.5105745132398615e-16, 1.3225682729326063),
        (0.0, 0.0, 2.0),
        (-0.6794171333284362, 1.4635754711956256e-16, 1.3225682557966318),
        (-0.35719063878059387, 7.444398803532795e-17, 1.322568167000891),
        (-0.35719063878059387, 0.0, 1.0993196964263916),
        (-0.6794169545173645, 0.0, 0.9351372122764587),
        (-0.9351372718811035, 0.0, 0.6794169545173645),
        (-1.0993198156356812, 0.0, 0.35719063878059387),
        (-1.1558932065963745, 0.0, 0.0),
        (-1.0993198156356812, 0.0, -0.3571906387805939),
        (-0.9351373314857483, 0.0, -0.6794170141220093),
        (-0.6794171333312987, 0.0, -0.9351373910903932),
        (-0.3571907579898834, 0.0, -1.0993200540542603),
        (-0.3571907579898834, 8.901813750307358e-17, -1.3530908315773076),
        (-0.6794171333341614, 1.5987273724709127e-16, -1.3530908315776538),
        (0.0, 0.0, -2.0),
        (0.6794172525418057, -1.5494454366804285e-16, -1.3530908315770325),
        (0.3527931571006775, -7.92686430293274e-17, -1.3530908278952074),
        (0.3571907579898834, 0.0, -1.0993201732635498),
        (0.6794172525405884, 0.0, -0.9351376295089722),
        (0.9351377156298226, 0.0, -0.679417149782752)
    ]
    cvTuples['Circle Three Arrows'] = [
        (0.0, 0.0, 2.0),
        (0.6794168353060688, 0.0, 1.3230991421415497),
        (0.3527929484844208, 0.0, 1.323098990664334),
        (0.3571905493736267, 0.0, 1.099319577217102),
        (0.679416835308075, 0.0, 0.935137152671814),
        (0.9351370930671692, 0.0, 0.6794168949127197),
        (1.099319577217102, 0.0, 0.3571905791759491),
        (1.4574850059366835, 0.0, 0.35279297828674316),
        (1.4574850564290887, 0.0, 0.6794168949127197),
        (2.1088373022076534, 0.0, 0.0),
        (1.45748535938352, 0.0, -0.6710525155067444),
        (1.4574855108607356, 0.0, -0.3571907877922058),
        (1.0993202924728394, 0.0, -0.3571907877922058),
        (0.9351376891136169, 0.0, -0.6794172525405884),
        (0.6794172525405884, 0.0, -0.9351376295089722),
        (0.3571907579898834, 0.0, -1.0993201732635498),
        (0.3527931571006775, 0.0, -1.3571294261079088),
        (0.6794168353100812, 0.0, -1.357129426106899),
        (0.0, 0.0, -2.0),
        (-0.6794169545181786, 0.0, -1.3571294261094236),
        (-0.3571907579898834, 0.0, -1.3571294261074038),
        (-0.3571907579898834, 0.0, -1.0993200540542603),
        (-0.6794171333312988, 0.0, -0.9351373910903931),
        (-0.9351373314857483, 0.0, -0.6794170141220093),
        (-1.0993198156356812, 0.0, -0.35719063878059387),
        (-1.1558932065963745, 0.0, 0.0),
        (-1.0993198156356812, 0.0, 0.35719063878059387),
        (-0.9351372718811035, 0.0, 0.6794169545173645),
        (-0.6794169545173645, 0.0, 0.9351372122764587),
        (-0.35719063878059387, 0.0, 1.0993196964263916),
        (-0.35719063878059387, 0.0, 1.3230991421415497),
        (-0.6794169545165505, 0.0, 1.323098990664334),
        (0.0, 0.0, 2.0)
    ]
    cvTuples['Circle Four Arrows'] = [
        (-2.1216866207846587, 0.0, 0.0),
        (-1.4913854205677681, 0.0, 0.6710521160554896),
        (-1.4913851613995965, 0.0, 0.35279303789138794),
        (-1.0993198156356812, 0.0, 0.35719063878059387),
        (-0.9351372718811035, 0.0, 0.6794169545173645),
        (-0.6794169545173645, 0.0, 0.9351372122764587),
        (-0.35719063878059387, 0.0, 1.0993196964263916),
        (-0.3577327673152563, 0.0, 1.3230746438305),
        (-0.6710524314567615, 0.0, 1.323074667217099),
        (0.0, 0.0, 2.0),
        (0.6794172913277731, 0.0, 1.3230746920038992),
        (0.34933833881456466, 0.0, 1.3230745922603877),
        (0.3571905493736267, 0.0, 1.099319577217102),
        (0.679416835308075, 0.0, 0.935137152671814),
        (0.9351370930671692, 0.0, 0.6794168949127197),
        (1.099319577217102, 0.0, 0.3571905791759491),
        (1.4549185759740928, 0.0, 0.3571905791759491),
        (1.454918773422636, 0.0, 0.6710521997022618),
        (2.1116996464337463, 0.0, 0.00108900412164048),
        (1.45491869482692, 0.0, -0.6794172107180964),
        (1.4549186058622896, 0.0, -0.3571907877922058),
        (1.0993202924728394, 0.0, -0.3571907877922058),
        (0.9351376891136169, 0.0, -0.6794172525405884),
        (0.6794172525405884, 0.0, -0.9351376295089722),
        (0.3571907579898834, 0.0, -1.0993201732635498),
        (0.3571907579898834, 0.0, -1.3572796680125012),
        (0.6794172137534037, 0.0, -1.3572795624146783),
        (0.0, 0.0, -2.0),
        (-0.6710523611381483, 0.0, -1.357279645230887),
        (-0.3571907579898834, 0.0, -1.3572798025873518),
        (-0.3571907579898834, 0.0, -1.0993200540542603),
        (-0.6794171333312988, 0.0, -0.9351373910903931),
        (-0.9351373314857483, 0.0, -0.6794170141220093),
        (-1.0993198156356812, 0.0, -0.35719063878059387),
        (-1.4913842573417506, 0.0, -0.35719063878059387),
        (-1.4913843596644172, 0.0, -0.6794172943630804),
        (-2.1216866207846587, 0.0, 0.0)
    ]
    cvTuples['Sphere Four Arrows'] = [
        (0.0, 0.0, -2.36394347671107),
        (0.7879811589036899, 0.0, -1.5759623178073798),
        (0.39399057945184496, 0.0, -1.5759623178073798),
        (0.38348088630589966, 0.0, -1.1802328196679974),
        (0.7294240678084163, 0.0, -1.003966094482852),
        (1.003966188417526, 0.0, -0.7294240678084163),
        (1.180233007537346, 0.0, -0.3834809097895682),
        (1.5759623178073798, 0.0, -0.39399057945184496),
        (1.5759623178073798, 0.0, -0.7879811589036899),
        (2.36394347671107, 0.0, 0.0),
        (1.5759623178073798, 0.0, 0.7879811589036899),
        (1.5759623178073798, 0.0, 0.39399057945184496),
        (1.1802322560599527, 0.0, 0.38348069843655147),
        (1.0039654369401332, 0.0, 0.7294236920697198),
        (0.7294235981350455, 0.0, 1.003965530874807),
        (0.38348065146921434, 0.0, 1.1802322560599527),
        (0.39399057945184496, 0.0, 1.5759623178073798),
        (0.7879811589036899, 0.0, 1.5759623178073798),
        (0.0, 0.0, 2.36394347671107),
        (-0.7879811589036899, 0.0, 1.5759623178073798),
        (-0.39399057945184496, 0.0, 1.5759623178073798),
        (-0.383480768887557, 0.0, 1.1802323499946268),
        (-0.7294237390370568, 0.0, 1.0039656248094813),
        (-1.0039657187441553, 0.0, 0.7294237390370568),
        (-1.1802325378639753, 0.0, 0.383480768887557),
        (-1.5759623178073798, 0.0, 0.39399057945184496),
        (-1.5759623178073798, 0.0, 0.7879811589036899),
        (-2.36394347671107, 0.0, 0.0),
        (-1.5759623178073798, 0.0, -0.7879811589036899),
        (-1.5759623178073798, 0.0, -0.39399057945184496),
        (-1.1802325378639753, 0.0, -0.383480768887557),
        (-1.0039658126788296, 0.0, -0.729423832971731),
        (-0.7294238799390679, 0.0, -1.0039658126788296),
        (-0.38348088630589966, 0.0, -1.1802327257333234),
        (-0.39399057945184496, 0.0, -1.5759623178073798),
        (-0.7879811589036899, 0.0, -1.5759623178073798),
        (0.0, 0.0, -2.36394347671107),
        (0.0, 0.7879811589036899, -1.5759623178073798),
        (0.0, 0.38348065146921434, -1.5759623178073798),
        (0.0, 0.38348065146921434, -1.1802328196679974),
        (0.0, 0.5633884255257395, -1.105712470050679),
        (0.0, 0.7294235981350455, -1.0039659066135038),
        (0.0, 0.8774979913768833, -0.877498461050254),
        (0.0, 1.0039654369401332, -0.7294239738737421),
        (0.0, 1.1057120003773087, -0.5633886603624247),
        (0.0, 1.1802322560599527, -0.38348088630589966),
        (0.0, 1.5759623178073798, -0.39399057945184496),
        (0.0, 1.5759623178073798, -0.7879811589036899),
        (0.0, 2.36394347671107, 0.0),
        (0.0, 1.5759623178073798, 0.7879811589036899),
        (0.0, 1.5759623178073798, 0.39399057945184496),
        (-1.1428615404264673e-08, 1.1802322560599527, 0.3834807454038885),
        (-1.679028348701416e-08, 1.1057120003773087, 0.5633884724930766),
        (-2.1738517228813336e-08, 1.0039654369401332, 0.7294236920697198),
        (-2.615147803356896e-08, 0.8774979913768833, 0.8774980853115575),
        (-2.992050161779324e-08, 0.7294235981350455, 1.0039656248094813),
        (-3.2952785503188034e-08, 0.5633884255257395, 1.1057120943119825),
        (-3.5173662187455676e-08, 0.38348065146921434, 1.1802323499946268),
        (-3.5173662187455676e-08, 0.38348065146921434, 1.5759623178073798),
        (-3.5173662187455676e-08, 0.7879811589036899, 1.5759623178073798),
        (-3.5173662187455676e-08, 0.0, 2.36394347671107),
        (-3.5173662187455676e-08, -0.7879811589036899, 1.5759623178073798),
        (-3.5173662187455676e-08, -0.38348065146921434, 1.5759623178073798),
        (-3.5173662187455676e-08, -0.38348065146921434, 1.1802323499946268),
        (-3.2952785503188034e-08, -0.5633884255257395, 1.1057120943119825),
        (-2.992050161779324e-08, -0.7294235981350455, 1.0039656248094813),
        (-2.615147803356896e-08, -0.8774979913768833, 0.8774980853115575),
        (-2.1738517228813336e-08, -1.0039654369401332, 0.7294236920697198),
        (-1.679028348701416e-08, -1.1057120003773087, 0.5633884724930766),
        (-1.1428615404264673e-08, -1.1802322560599527, 0.3834807454038885),
        (-1.1428615404264673e-08, -1.5759623178073798, 0.39399057945184496),
        (-1.1428615404264673e-08, -1.5759623178073798, 0.7879811589036899),
        (-1.1428615404264673e-08, -2.36394347671107, 0.0),
        (-0.7879811589036899, -1.5759623178073798, 0.0),
        (-0.39399057945184496, -1.5759623178073798, 0.0),
        (-0.383480768887557, -1.1802322560599527, 0.0),
        (-0.5633885664277506, -1.1057120003773087, 0.0),
        (-0.7294237390370568, -1.0039654369401332, 0.0),
        (-0.8774981792462315, -0.8774979913768833, 0.0),
        (-1.0039657187441553, -0.7294235981350455, 0.0),
        (-1.1057122821813308, -0.5633884255257395, 0.0),
        (-1.1802325378639753, -0.38348065146921434, 0.0),
        (-1.5759623178073798, -0.38348065146921434, 0.0),
        (-1.5759623178073798, -0.7879811589036899, 0.0),
        (-2.36394347671107, 0.0, 0.0),
        (-1.5759623178073798, 0.7879811589036899, 0.0),
        (-1.5759623178073798, 0.38348065146921434, 0.0),
        (-1.1802325378639753, 0.38348065146921434, 0.0),
        (-1.1057122821813308, 0.5633884255257395, 0.0),
        (-1.0039657187441553, 0.7294235981350455, 0.0),
        (-0.8774981792462315, 0.8774979913768833, 0.0),
        (-0.7294237390370568, 1.0039654369401332, 0.0),
        (-0.5633885664277506, 1.1057120003773087, 0.0),
        (-0.383480768887557, 1.1802322560599527, 0.0),
        (-0.39399057945184496, 1.5759623178073798, 0.0),
        (-0.7879811589036899, 1.5759623178073798, 0.0),
        (0.0, 2.36394347671107, 0.0),
        (0.7879811589036899, 1.5759623178073798, 0.0),
        (0.39399057945184496, 1.5759623178073798, 0.0),
        (0.38348069843655147, 1.1802322560599527, 0.0),
        (0.5633884255257395, 1.1057120003773087, 0.0),
        (0.7294235981350455, 1.0039654369401332, 0.0),
        (0.8774979913768833, 0.8774979913768833, 0.0),
        (1.0039654369401332, 0.7294235981350455, 0.0),
        (1.1057120003773087, 0.5633884255257395, 0.0),
        (1.1802322560599527, 0.38348065146921434, 0.0),
        (1.5759623178073798, 0.38348065146921434, 0.0),
        (1.5759623178073798, 0.7879811589036899, 0.0),
        (2.36394347671107, 0.0, 0.0),
        (1.5759623178073798, -0.7879811589036899, 0.0),
        (1.5759623178073798, -0.38348065146921434, 0.0),
        (1.1802322560599527, -0.38348065146921434, 0.0),
        (1.1057120003773087, -0.5633884255257395, 0.0),
        (1.0039654369401332, -0.7294235981350455, 0.0),
        (0.8774979913768833, -0.8774979913768833, 0.0),
        (0.7294235981350455, -1.0039654369401332, 0.0),
        (0.5633884255257395, -1.1057120003773087, 0.0),
        (0.38348069843655147, -1.1802322560599527, 0.0),
        (0.39399057945184496, -1.5759623178073798, 0.0),
        (0.7879811589036899, -1.5759623178073798, 0.0),
        (0.0, -2.36394347671107, 0.0),
        (0.0, -1.5759623178073798, -0.7879811589036899),
        (0.0, -1.5759623178073798, -0.39399057945184496),
        (0.0, -1.1802322560599527, -0.38348088630589966),
        (0.0, -1.1057120003773087, -0.5633886603624247),
        (0.0, -1.0039654369401332, -0.7294239738737421),
        (0.0, -0.8774979913768833, -0.877498461050254),
        (0.0, -0.7294235981350455, -1.0039659066135038),
        (0.0, -0.5633884255257395, -1.105712470050679),
        (0.0, -0.38348065146921434, -1.1802328196679974),
        (0.0, -0.38348065146921434, -1.5759623178073798),
        (0.0, -0.7879811589036899, -1.5759623178073798),
        (0.0, 0.0, -2.36394347671107)
    ]
    cvTuples['Gear'] = [
        (-0.1831451367158871, 0.0, -1.9688981435835975),
        (-0.08016223035760504, 0.0, -1.424910142313325),
        (0.2913626899858565, 0.0, -1.397105097768184),
        (0.6430317256821292, 0.0, -1.2740896471493144),
        (0.954867881657974, 0.0, -1.7315681158569183),
        (1.3166068046861326, 0.0, -1.4735764149704769),
        (1.6135439258005473, 0.0, -1.1430580934022687),
        (1.1939272305203956, 0.0, -0.781877785172391),
        (1.355609846159615, 0.0, -0.4462249772153243),
        (1.4249099319855256, 0.0, -0.08016261435117376),
        (1.9770167544414288, 0.0, -0.038844183867340044),
        (1.9344591432773475, 0.0, 0.40342536276371044),
        (1.7966906553990056, 0.0, 0.825839198145925),
        (1.2740908453616502, 0.0, 0.6430325043934684),
        (1.064247138807185, 0.0, 0.9508803230361444),
        (0.7818781368370868, 0.0, 1.1939274851034107),
        (1.0221485601850735, 0.0, 1.6927255501307752),
        (0.6178520249074239, 0.0, 1.8770034010800105),
        (0.18314513671588942, 0.0, 1.968898382002176),
        (0.08016221299102935, 0.0, 1.4249104640058996),
        (-0.29136272471900787, 0.0, 1.397105502734753),
        (-0.6430317777818587, 0.0, 1.274090135389879),
        (-0.9548679511242792, 0.0, 1.7315686873714762),
        (-1.316606804686128, 0.0, 1.4735766533890562),
        (-1.6135439258005448, 0.0, 1.1430583318208474),
        (-1.1939272478869714, 0.0, 0.7818781068649654),
        (-1.355609828793037, 0.0, 0.44622513235990835),
        (-1.4249098972523697, 0.0, 0.08016268622176266),
        (-1.9770167023416967, 0.0, 0.03884417246393463),
        (-1.9344588458747152, 0.0, -0.40342655041229425),
        (-1.7966888454342211, 0.0, -0.8258409718969756),
        (-1.2740894521947093, 0.0, -0.6430322795686422),
        (-1.0642471040740267, 0.0, -0.9508802511655553),
        (-0.7818781194705111, 0.0, -1.1939273299588267),
        (-1.0221485254519176, 0.0, -1.692725478260187),
        (-0.6178520249074192, 0.0, -1.8770031626614314),
        (-0.1831451367158871, 0.0, -1.9688981435835975)
    ]