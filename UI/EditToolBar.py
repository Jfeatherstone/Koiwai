import sys
from PyQt5 import QtWidgets, QtCore, QtGui

POINTER_TOOL = "pointer"
MOVE_TOOL = "move"
ROTATE_TOOL = "rotate"
RESET_TOOL = "reset"
ZOOM_TOOL = "zoom"

class EditToolBar(QtWidgets.QToolBar):

    toolClickSgl = QtCore.pyqtSignal(str)

    def __init__(self):

        super(EditToolBar, self).__init__('Edit')

        self.toolButtonGroup = QtWidgets.QButtonGroup()

        self.undoTool = QtWidgets.QAction(QtGui.QIcon(':undo'), '&Undo')

        self.resetViewTool = QtWidgets.QAction(QtGui.QIcon(':square'), '&Reset View')
        self.resetViewTool.triggered.connect(self._clickReset)

        self.moveTool = QtWidgets.QToolButton()
        self.moveTool.setIcon(QtGui.QIcon(':move'))
        self.moveTool.setCheckable(True)
        self.moveTool.setToolTip('Move')
        self.moveTool.clicked.connect(self._clickMove)
        self.toolButtonGroup.addButton(self.moveTool) 

        self.rotateTool = QtWidgets.QToolButton()
        self.rotateTool.setIcon(QtGui.QIcon(':sync'))
        self.rotateTool.setCheckable(True)
        self.rotateTool.setToolTip('Rotate')
        self.rotateTool.clicked.connect(self._clickRotate)
        self.toolButtonGroup.addButton(self.rotateTool) 

        self.zoomInTool = QtWidgets.QAction(QtGui.QIcon(':maximize'), '&Zoom In')
        self.zoomOutTool = QtWidgets.QAction(QtGui.QIcon(':minimize'), '&Zoom Out')

        self.addAction(self.undoTool)
        self.addAction(self.resetViewTool)
        
        self.addWidget(self.moveTool)
        self.addWidget(self.rotateTool)
        self.addAction(self.zoomInTool)
        self.addAction(self.zoomOutTool)


    def _clickMove(self, event):
        if self.moveTool.isChecked():
            self.toolClickSgl.emit(MOVE_TOOL)

    def _clickRotate(self, event):
        if self.rotateTool.isChecked():
            self.toolClickSgl.emit(ROTATE_TOOL)

    def _clickReset(self, event):
        # No need to verify checked status, since this isn't a tool
        self.toolClickSgl.emit(RESET_TOOL)


