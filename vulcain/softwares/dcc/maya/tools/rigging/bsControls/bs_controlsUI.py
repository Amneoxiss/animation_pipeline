'''

Control Curves Tool made by Brandon Schaal

This file is simply the GUI that handles user input and calls all functionality and data from the bs_controls.py file. A more 
detailed explanation of the tool can be found in the bs_controls.py file.

'''

import maya.cmds as cmds
import bs_controls as bsCon

reload(bsCon)
bsUtils = bsCon.BSControlsUtils()
bsData = bsCon.BSControlsData()

class BSControlsUI():
    # Function to create the UI
    def bsControlsUI(self, *args):
        # Dictionary to store UI elements
        self.UIElements = {}
        # Checks to see if the UI exists
        windowName = 'bsControls'
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)
        # Defining default window and button dimensions
        windowWidth = 260
        windowHeight = 436
        cX = (windowWidth-15)/30
        cY = 32/cX

        # Create all elements for the GUI
        self.UIElements['conWindow'] = cmds.window(windowName, width=windowWidth, height=windowHeight, title='bsControls', sizeable=True)
        
        # Main parent form and column
        self.UIElements['conFormLayout'] = cmds.formLayout(nd=100)
        self.UIElements['conColumn'] = cmds.columnLayout(p=self.UIElements['conFormLayout'])

        # Create Controls frame and children
        self.UIElements['conCreateFrameLayout'] = cmds.frameLayout(l='Create Controls', bgc=[0.1, 0.2, 0.3], cll=True, w=windowWidth, p=self.UIElements['conColumn'])
        self.UIElements['conCreateFormLayout'] = cmds.formLayout(nd=100, p=self.UIElements['conCreateFrameLayout'])
        self.UIElements['conCreateRowColumn'] = cmds.rowColumnLayout(p=self.UIElements['conCreateFormLayout'], bgc=[0.2, 0.2, 0.2], nr=6, rs=[(1,1),(2,5),(3,5),(4,5),(5,5),(6,5)])

        self.UIElements['conCreateNameColumn'] = cmds.rowColumnLayout(p=self.UIElements['conCreateRowColumn'], bgc=[0.2, 0.2, 0.2], nc=3, cw=[(1,1),(2,windowWidth-6),(3,1)])
        cmds.separator(st='none', p=self.UIElements['conCreateNameColumn'])
        self.UIElements['conCreateName'] = cmds.textField(pht='Controller name or suffix replace...', ann='Name the created controls or just replace the suffix of the selected object\'s name',
             bgc=[0.1, 0.1, 0.1], p=self.UIElements['conCreateNameColumn'])
        cmds.separator(st='none', p=self.UIElements['conCreateNameColumn'])

        self.UIElements['conCreateThickColumn'] = cmds.rowColumnLayout(p=self.UIElements['conCreateRowColumn'], bgc=[0.2, 0.2, 0.2], nc=3, cw=[(1,1),(2,windowWidth-6),(3,1)])
        cmds.separator(st='none', p=self.UIElements['conCreateThickColumn'])
        self.UIElements['conCreateThick'] = cmds.floatSliderGrp(p=self.UIElements['conCreateThickColumn'], field=True, l='Thickness', v=1.0, min=1.0, max=8.0, 
            cw=[(1,55),(2,30),(3,windowWidth-85)], pre=1)
        cmds.separator(st='none', p=self.UIElements['conCreateThickColumn'])
        
        self.UIElements['conCreateListColumn'] = cmds.rowColumnLayout(p=self.UIElements['conCreateRowColumn'], bgc=[0.2, 0.2, 0.2], nc=3, cw=[(1,1),(2,windowWidth-6),(3,1)])
        cmds.separator(st='none', p=self.UIElements['conCreateListColumn'])
        self.UIElements['conCreateList'] = cmds.textScrollList(h=135, p=self.UIElements['conCreateListColumn'], ams=False, ebg=True, bgc=[0.2, 0.2, 0.2], sii=1, append=bsData.controlNames)
        cmds.separator(st='none', p=self.UIElements['conCreateListColumn'])

        self.UIElements['conCreateBtnColumn1'] = cmds.rowColumnLayout(p=self.UIElements['conCreateRowColumn'], bgc=[0.2, 0.2, 0.2], nc=4, 
            cw=[(1,windowWidth*0.48),(2,windowWidth*0.04),(3,windowWidth*0.465),(4,1)])
        self.UIElements['conCreateParBtn'] = cmds.button(l='Parent', bgc=[0.4, 0.4, 0.4], c=self.bsParentBtn, p=self.UIElements['conCreateBtnColumn1'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn1'])
        self.UIElements['conCreateChldBtn'] = cmds.button(l='Child', bgc=[0.4, 0.4, 0.4], c=self.bsChildBtn, p=self.UIElements['conCreateBtnColumn1'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn1'])

        self.UIElements['conCreateBtnColumn2'] = cmds.rowColumnLayout(p=self.UIElements['conCreateRowColumn'], bgc=[0.2, 0.2, 0.2], nc=4, 
            cw=[(1,windowWidth*0.48),(2,windowWidth*0.04),(3,windowWidth*0.465),(4,1)])
        self.UIElements['conCreateWrldBtn'] = cmds.button(l='World', bgc=[0.4, 0.4, 0.4], c=self.bsWorldBtn, p=self.UIElements['conCreateBtnColumn2'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn2'])
        self.UIElements['conCreateOriginBtn'] = cmds.button(l='Origin', bgc=[0.4, 0.4, 0.4], c=self.bsOriginBtn, p=self.UIElements['conCreateBtnColumn2'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn2'])

        #Test Try new Column
        self.UIElements['conCreateBtnColumn3'] = cmds.rowColumnLayout(p=self.UIElements['conCreateRowColumn'], bgc=[0.2, 0.2, 0.2], nc=6, 
            cw=[(1,windowWidth*0.3),(2,windowWidth*0.04),(3,windowWidth*0.3),(4,windowWidth*0.04), (5,windowWidth*0.3), (6,1)])
        self.UIElements['conCreateCenterBtn'] = cmds.button(l='Center', bgc=[0.4, 0.4, 0.4], c=self.bsCenterBtn, p=self.UIElements['conCreateBtnColumn3'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn3'])
        self.UIElements['conCreateLeftBtn'] = cmds.button(l='Left', bgc=[0.4, 0.4, 0.4], c=self.bsLeftBtn, p=self.UIElements['conCreateBtnColumn3'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn3'])
        self.UIElements['conCreateRightBtn'] = cmds.button(l='Right', bgc=[0.4, 0.4, 0.4], c=self.bsRightBtn, p=self.UIElements['conCreateBtnColumn3'])
        cmds.separator(st='none', p=self.UIElements['conCreateBtnColumn3'])

        # Control Colors frame and children
        self.UIElements['conColorsFrameLayout'] = cmds.frameLayout(l='Control Colors', bgc=[0.1, 0.2, 0.3], cll=True, w=windowWidth, p=self.UIElements['conColumn'])
        self.UIElements['conColorsFormLayout'] = cmds.formLayout(nd=100, p=self.UIElements['conColorsFrameLayout'])
        self.UIElements['conColorsColumn'] = cmds.columnLayout(p=self.UIElements['conColorsFormLayout'], co=['left', 8], bgc=[0.2, 0.2, 0.2])
        cmds.separator(st='none', p=self.UIElements['conColorsColumn'])
        self.UIElements['conColorsGrid'] = cmds.gridLayout(w=windowWidth-10, h=(cY*20)+5, nr=cY, nc=cX, cwh=[30, 20], p=self.UIElements['conColorsColumn'])
        cmds.iconTextButton(bgc=[0, 0.016, 0.373], rpt=True, c=lambda: self.bsSetIndexBtn(0), dcc=lambda: self.bsSetIndexBtn(0))
        cmds.iconTextButton(bgc=[0, 0, 0], rpt=True, c=lambda: self.bsSetIndexBtn(1), dcc=lambda: self.bsSetIndexBtn(1))
        cmds.iconTextButton(bgc=[0.247, 0.247, 0.247], rpt=True, c=lambda: self.bsSetIndexBtn(2), dcc=lambda: self.bsSetIndexBtn(2))
        cmds.iconTextButton(bgc=[0.498, 0.498, 0.498], rpt=True, c=lambda: self.bsSetIndexBtn(3), dcc=lambda: self.bsSetIndexBtn(3))
        cmds.iconTextButton(bgc=[0.608, 0, 0.157], rpt=True, c=lambda: self.bsSetIndexBtn(4), dcc=lambda: self.bsSetIndexBtn(4))
        cmds.iconTextButton(bgc=[0, 0, 1], rpt=True, c=lambda: self.bsSetIndexBtn(6), dcc=lambda: self.bsSetIndexBtn(6))
        cmds.iconTextButton(bgc=[0, 0.275, 0.094], rpt=True, c=lambda: self.bsSetIndexBtn(7), dcc=lambda: self.bsSetIndexBtn(7))
        cmds.iconTextButton(bgc=[0.145, 0, 0.263], rpt=True, c=lambda: self.bsSetIndexBtn(8), dcc=lambda: self.bsSetIndexBtn(8))
        cmds.iconTextButton(bgc=[0.78, 0, 0.78], rpt=True, c=lambda: self.bsSetIndexBtn(9), dcc=lambda: self.bsSetIndexBtn(9))
        cmds.iconTextButton(bgc=[0.537, 0.278, 0.2], rpt=True, c=lambda: self.bsSetIndexBtn(10), dcc=lambda: self.bsSetIndexBtn(10))
        cmds.iconTextButton(bgc=[0.243, 0.133, 0.122], rpt=True, c=lambda: self.bsSetIndexBtn(11), dcc=lambda: self.bsSetIndexBtn(11))
        cmds.iconTextButton(bgc=[0.6, 0.145, 0], rpt=True, c=lambda: self.bsSetIndexBtn(12), dcc=lambda: self.bsSetIndexBtn(12))
        cmds.iconTextButton(bgc=[1, 0, 0], rpt=True, c=lambda: self.bsSetIndexBtn(13), dcc=lambda: self.bsSetIndexBtn(13))
        cmds.iconTextButton(bgc=[0, 1, 0], rpt=True, c=lambda: self.bsSetIndexBtn(14), dcc=lambda: self.bsSetIndexBtn(14))
        cmds.iconTextButton(bgc=[0, 0.255, 0.6], rpt=True, c=lambda: self.bsSetIndexBtn(15), dcc=lambda: self.bsSetIndexBtn(15))
        cmds.iconTextButton(bgc=[1, 1, 1], rpt=True, c=lambda: self.bsSetIndexBtn(16), dcc=lambda: self.bsSetIndexBtn(16))
        cmds.iconTextButton(bgc=[1, 1, 0], rpt=True, c=lambda: self.bsSetIndexBtn(17), dcc=lambda: self.bsSetIndexBtn(17))
        cmds.iconTextButton(bgc=[0.388, 0.863, 1], rpt=True, c=lambda: self.bsSetIndexBtn(18), dcc=lambda: self.bsSetIndexBtn(18))
        cmds.iconTextButton(bgc=[0.263, 1, 0.635], rpt=True, c=lambda: self.bsSetIndexBtn(19), dcc=lambda: self.bsSetIndexBtn(19))
        cmds.iconTextButton(bgc=[1, 0.686, 0.686], rpt=True, c=lambda: self.bsSetIndexBtn(20), dcc=lambda: self.bsSetIndexBtn(20))
        cmds.iconTextButton(bgc=[0.89, 0.675, 0.475], rpt=True, c=lambda: self.bsSetIndexBtn(21), dcc=lambda: self.bsSetIndexBtn(21))
        cmds.iconTextButton(bgc=[1, 1, 0.384], rpt=True, c=lambda: self.bsSetIndexBtn(22), dcc=lambda: self.bsSetIndexBtn(22))
        cmds.iconTextButton(bgc=[0, 0.6, 0.325], rpt=True, c=lambda: self.bsSetIndexBtn(23), dcc=lambda: self.bsSetIndexBtn(23))
        cmds.iconTextButton(bgc=[0.627, 0.412, 0.188], rpt=True, c=lambda: self.bsSetIndexBtn(24), dcc=lambda: self.bsSetIndexBtn(24))
        cmds.iconTextButton(bgc=[0.62, 0.627, 0.188], rpt=True, c=lambda: self.bsSetIndexBtn(25), dcc=lambda: self.bsSetIndexBtn(25))
        cmds.iconTextButton(bgc=[0.408, 0.627, 0.188], rpt=True, c=lambda: self.bsSetIndexBtn(26), dcc=lambda: self.bsSetIndexBtn(26))
        cmds.iconTextButton(bgc=[0.188, 0.627, 0.365], rpt=True, c=lambda: self.bsSetIndexBtn(27), dcc=lambda: self.bsSetIndexBtn(27))
        cmds.iconTextButton(bgc=[0.188, 0.627, 0.627], rpt=True, c=lambda: self.bsSetIndexBtn(28), dcc=lambda: self.bsSetIndexBtn(28))
        cmds.iconTextButton(bgc=[0.188, 0.404, 0.627], rpt=True, c=lambda: self.bsSetIndexBtn(29), dcc=lambda: self.bsSetIndexBtn(29))
        cmds.iconTextButton(bgc=[0.435, 0.188, 0.627], rpt=True, c=lambda: self.bsSetIndexBtn(30), dcc=lambda: self.bsSetIndexBtn(30))
        cmds.iconTextButton(st='iconAndTextHorizontal', l='T', bgc=[0.498, 0.498, 0.498], rpt=True, c=lambda: self.bsSetDisplayTypeBtn(1), dcc=lambda: self.bsSetDisplayTypeBtn(1))
        cmds.iconTextButton(st='iconAndTextHorizontal', l='R', bgc=[0, 0, 0], rpt=True, c=lambda: self.bsSetDisplayTypeBtn(2), dcc=lambda: self.bsSetDisplayTypeBtn(2))
        cmds.iconTextButton(st='textOnly', l='Reset Color', rpt=True, bgc=[0.4, 0.4, 0.4], w=windowWidth-20, c=self.bsResetColorBtn, p=self.UIElements['conColorsColumn'])
        cmds.separator(p=self.UIElements['conColorsColumn'])

        # Replace Controller Shapes frame and children
        self.UIElements['conShapeFrameLayout'] = cmds.frameLayout(l='Control Shape Replace', bgc=[0.1, 0.2, 0.3], cll=True, w=windowWidth, p=self.UIElements['conColumn'])
        self.UIElements['conShapeFormLayout'] = cmds.formLayout(nd=100, p=self.UIElements['conShapeFrameLayout'])
        self.UIElements['conShapeRowColumn'] = cmds.rowColumnLayout(p=self.UIElements['conShapeFormLayout'], bgc=[0.2, 0.2, 0.2], nr=15, rs=[(1,2),(2,2),(3,2),(4,7),(5,2),(6,7),(7,2),(8,2),(9,2),(10,2),(11,2)])
        
        self.UIElements['conShapeTextColumn'] = cmds.rowColumnLayout(p=self.UIElements['conShapeRowColumn'], bgc=[0.2, 0.2, 0.2], nc=4, 
            cw=[(1,windowWidth*0.48),(2,windowWidth*0.04),(3,windowWidth*0.465),(4,1)])
        self.UIElements['conShapeReplace'] = cmds.textField(pht='Shapes to replace...', p=self.UIElements['conShapeTextColumn'], bgc=[0.1, 0.1, 0.1], ed=False)
        cmds.separator(st='none', p=self.UIElements['conShapeTextColumn'])
        self.UIElements['conShapeReplacement'] = cmds.textField(pht='Replacement(s)...', p=self.UIElements['conShapeTextColumn'], bgc=[0.1, 0.1, 0.1], ed=False)
        cmds.separator(st='none', p=self.UIElements['conShapeTextColumn'])

        self.UIElements['conShapeTextBtnColumn'] = cmds.rowColumnLayout(p=self.UIElements['conShapeRowColumn'], bgc=[0.2, 0.2, 0.2], nc=4, 
            cw=[(1,windowWidth*0.48), (2,windowWidth*0.04), (3,windowWidth*0.465),(4,1)])
        self.UIElements['conShapeLoadBtn'] = cmds.button(l='Load Shape', bgc=[0.4, 0.4, 0.4], c=self.bsLoadTargetBtn, p=self.UIElements['conShapeTextBtnColumn'])
        cmds.separator(st='none', p=self.UIElements['conShapeTextBtnColumn'])
        self.UIElements['conShapeReplacementBtn'] = cmds.button(l='Load Replacement', bgc=[0.4, 0.4, 0.4], c=self.bsLoadReplaceBtn, p=self.UIElements['conShapeTextBtnColumn'])
        cmds.separator(st='none', p=self.UIElements['conShapeTextBtnColumn'])

        cmds.separator(st='none', p=self.UIElements['conShapeRowColumn'])

        self.UIElements['conShapeMirrorColumn'] = cmds.rowColumnLayout(p=self.UIElements['conShapeRowColumn'], bgc=[0.2, 0.2, 0.2], nc=3, 
            cw=[(1,windowWidth*0.3),(2,windowWidth*0.5),(3,windowWidth*0.01)])
        cmds.separator(st='none', p=self.UIElements['conShapeMirrorColumn'])
        self.UIElements['conShapeMirror'] = cmds.checkBox(p=self.UIElements['conShapeMirrorColumn'], l='Mirror Shapes', v=False)
        cmds.separator(st='none', p=self.UIElements['conShapeMirrorColumn'])

        cmds.separator(st='none', p=self.UIElements['conShapeRowColumn'])

        self.UIElements['conShapeReplaceBtn'] = cmds.button(l='Replace Shapes', bgc=[0.4, 0.4, 0.4], w=windowWidth-10, c=self.bsReplaceShapeBtn, p=self.UIElements['conShapeRowColumn'])
        cmds.separator(st='none', p=self.UIElements['conShapeRowColumn'])

         
        #Mirror Button
        self.UIElements['conShapeMirrorButton'] = cmds.button(l='Mirror', bgc=[0.4, 0.4, 0.4], w=windowWidth-10, c=self.bsMirrorBtn, p=self.UIElements['conShapeRowColumn'])        
        cmds.separator(st='none', p=self.UIElements['conShapeRowColumn'])

        #Parent jnt to ctrl button
        self.UIElements['conShapeParentCtrlJntButton'] = cmds.button(l='Parent ctrl', bgc=[0.4, 0.4, 0.4], w=windowWidth-10, c=self.bsParentCtrlJntBtn, p=self.UIElements['conShapeRowColumn'])
        
        cmds.separator(st='none', p=self.UIElements['conShapeRowColumn'])

        # Format and display GUI window
        cmds.formLayout(self.UIElements['conFormLayout'], e=True, af=[(self.UIElements['conColumn'], 'top', 3),(
        self.UIElements['conColumn'], 'left', 1)])
        cmds.formLayout(self.UIElements['conCreateFormLayout'], e=True, af=[(self.UIElements['conCreateRowColumn'], 'top', 2),(
        self.UIElements['conCreateRowColumn'], 'left', 1)])
        cmds.formLayout(self.UIElements['conColorsFormLayout'], e=True, af=[(self.UIElements['conColorsColumn'], 'top', 2),(
        self.UIElements['conColorsColumn'], 'left', 1)])
        cmds.formLayout(self.UIElements['conShapeFormLayout'], e=True, af=[(self.UIElements['conShapeRowColumn'], 'top', 2),(
        self.UIElements['conShapeRowColumn'], 'left', 1)])
        cmds.showWindow(windowName)

    # Function to get user input for curve data.
    def bsGetCurveData(self, *args):
        curve = cmds.textScrollList(self.UIElements['conCreateList'], q=True, si=True)
        name = cmds.textField(self.UIElements['conCreateName'], q=True, tx=True)
        thickness = cmds.floatSliderGrp(self.UIElements['conCreateThick'], q=True, v=True)

        return [curve, name, thickness]

    # Function for the Parent button to create control curve(s) as a parent to the selected object(s).
    def bsParentBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('parent', data[0], data[1], data[2])

    # Function for the Child button to create control curve(s) as a child to the selected object(s).
    def bsChildBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('child', data[0], data[1], data[2])

    # Function for the World button to create control curve(s) as a child of the world at the selected object(s).
    def bsWorldBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('world', data[0], data[1], data[2])

    # Function for the Origin button to create a control curve at the origin.
    def bsOriginBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('origin', data[0], data[1], data[2])

    def bsCenterBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('center', data[0], data[1], data[2])

    def bsLeftBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('left', data[0], data[1], data[2])

    def bsRightBtn(self, *args):
        data = self.bsGetCurveData()
        bsUtils.bsPlaceControls('right', data[0], data[1], data[2])

    # Function for the color grid buttons.
    def bsSetIndexBtn(self, color):
        bsUtils.bsSetIndex(color)

    # Function for the T and R color grid buttons.
    def bsSetDisplayTypeBtn(self, display):
        bsUtils.bsSetDisplayType(display)

    # Function for the reset color button.
    def bsResetColorBtn(self, *args):
        bsUtils.bsResetColor()

    # Function for load shape button.
    def bsLoadTargetBtn(self, *args):
        self.targetShapes = bsUtils.bsLoadShapes(self.UIElements['conShapeReplace']) 

    # Function for load replacement button.
    def bsLoadReplaceBtn(self, *args):
        self.replacementShapes = bsUtils.bsLoadShapes(self.UIElements['conShapeReplacement'])

    # Function for replace shape button that checks how to use repalceShape function.
    def bsReplaceShapeBtn(self, *args):
        # Checking to make sure shapes have been loaded.
        replacements = cmds.textField(self.UIElements['conShapeReplacement'], q=True, tx=True)
        shapes = cmds.textField(self.UIElements['conShapeReplace'], q=True, tx=True)
        mirror = cmds.checkBox(self.UIElements['conShapeMirror'], q=True, v=True)

        if replacements == '':
            cmds.error('No replacement shapes have been selected and loaded.')
        if shapes == '':
            cmds.error('No target shapes have been selected and loaded.')

        # Logic for how to run bsReplaceShape function
        replacementLen = len(self.replacementShapes)
        targetLen = len(self.targetShapes)

        if replacementLen > 1:
            if replacementLen == targetLen:
                for r in range(replacementLen):
                    bsUtils.bsReplaceShape(self.targetShapes[r], self.replacementShapes[r], mirror)
            else:
                cmds.error('Amount of target and replacement shapes do not match. Select only 1 or the same number of replacement shapes as targets.')
        else:
            for r in range(targetLen):
                bsUtils.bsReplaceShape(self.targetShapes[r], self.replacementShapes[0], mirror)

    def bsMirrorBtn(self, *args):
        bsUtils.bsMirror()

    def bsParentCtrlJntBtn(self, *args):
        bsUtils.bsParentCtrlJnt()
