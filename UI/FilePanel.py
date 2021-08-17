import sys
import os
from pathlib import Path

from UI.Config import settings

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

DEFAULT_WIDTH = 250

class FilePane(QtWidgets.QWidget):

    # The string we will be sending is the file path
    fileClickSgl = QtCore.pyqtSignal(str)

    def __init__(self, startDirectory, parent=None):
        super(FilePane, self).__init__(parent)

        self.currentDirectory = startDirectory

        self.showHiddenFiles = settings["showHiddenFiles"]
        self.showNonImageFiles = settings["showNonImageFiles"]

        self.resize(DEFAULT_WIDTH, self.sizeHint().height())

        # Simple vertical stacking of the elements
        self.layout = QtWidgets.QVBoxLayout()

        # Button to change the current directory
        self.dirSelectBtn= QtWidgets.QPushButton("Select Directory")
        self.dirSelectBtn.clicked.connect(self.selectDirectory)

        self.layout.addWidget(self.dirSelectBtn)

        # The label for the current directory
        self.currentDirLbl = QtWidgets.QLabel() 
        self.currentDirLbl.setText('Current Directory:\n' + startDirectory)
        self.currentDirLbl.setAlignment(Qt.Qt.AlignCenter)
        self.layout.addWidget(self.currentDirLbl)

        # Put the refresh button next to the two checkboxes, so we need another
        # horizontal layout
        self.fileOptionsLayout = QtWidgets.QHBoxLayout()

        self.checkBoxLayout = QtWidgets.QVBoxLayout()

        # Checkbox to show hidden files
        self.showHiddenFilesChBx = QtWidgets.QCheckBox('Show hidden files')
        self.showHiddenFilesChBx.setChecked(self.showHiddenFiles)
        self.showHiddenFilesChBx.stateChanged.connect(self._toggleShowHiddenFiles)
        self.checkBoxLayout.addWidget(self.showHiddenFilesChBx)

        # Checkbox to show non image files
        self.showNonImageFilesChBx = QtWidgets.QCheckBox('Show non-image files')
        self.showNonImageFilesChBx.setChecked(self.showNonImageFiles)
        self.showNonImageFilesChBx.stateChanged.connect(self._toggleShowNonImageFiles)
        self.checkBoxLayout.addWidget(self.showNonImageFilesChBx)

        self.fileOptionsLayout.addLayout(self.checkBoxLayout)

        # The refresh button
        self.refreshBtn = QtWidgets.QPushButton()
        self.refreshBtn.setIcon(QtGui.QIcon('assets/icons/sync-outline.svg'))
        self.refreshBtn.setMaximumWidth(40)
        self.refreshBtn.clicked.connect(lambda x: self.updateFileList(self.currentDirectory))
        self.fileOptionsLayout.addWidget(self.refreshBtn)

        self.layout.addLayout(self.fileOptionsLayout)
    
        # The list of files in the current directory
        self.fileLst = QtWidgets.QListWidget()
        self.fileLst.setSortingEnabled(True)
        self.fileLst.itemActivated.connect(self._onListItemClick)

        self.layout.addWidget(self.fileLst)

        #self.contents = QTextEdit()
        #layout.addWidget(self.contents)
        self.setLayout(self.layout)
        self.setWindowTitle("File Panel")

        self.updateFileList(startDirectory)


    def selectDirectory(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory', self.currentDirectory)

        self.updateFileList(dirName)


    def updateFileList(self, newDirectory):
        if len(newDirectory) > 0:# and newDirectory != self.currentDirectory:
            self.currentDirLbl.setText('Current Directory:\n' + newDirectory)
            self.currentDirectory = newDirectory

            # First, clear the list
            self.fileLst.clear()

            # Now add all of the new items
            fileArr = os.listdir(self.currentDirectory)
            self.fileLst.addItem('..')

            # Remove hidden files if applicable
            if not self.showHiddenFiles:
                fileArr = [f for f in fileArr if f[0] != '.']

            # Remove non image files if applicable
            if not self.showNonImageFiles:
                fileArr = [f for f in fileArr if Path(self.currentDirectory + '/' + f).suffix[1:] in settings["imageFileTypes"]]

            self.fileLst.addItems(fileArr)
            return

    # Decorator indicates that this will be used to signal an event in another widget
    # (in the ImagePane, to be specific)
    @QtCore.pyqtSlot()
    def _onListItemClick(self):
        fileName = self.fileLst.currentItem().text()

        if fileName == '..':
            self.updateFileList(str(Path(self.currentDirectory).parent))
            return

        #print(self.currentDirectory + '/' + item.text())
        # If we have selected a directory, we can change that to be the active directory
        if os.path.isdir(self.currentDirectory + '/' + fileName):
            self.updateFileList(str(Path(self.currentDirectory + '/' + fileName)))
            return

        # Otherwise, we open the image in the viewer pane
        if len(fileName) > 0:
            self.fileClickSgl.emit(self.currentDirectory + '/' + fileName)
            return
            
	
    def _toggleShowHiddenFiles(self, state):

        # Update the state var and then refresh the list
        self.showHiddenFiles = state == QtCore.Qt.Checked 
        self.updateFileList(self.currentDirectory)

    def _toggleShowNonImageFiles(self, state):

        self.showNonImageFiles = state == QtCore.Qt.Checked
        self.updateFileList(self.currentDirectory)
