import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

DEFAULT_WIDTH = 250

class FileDialogPane(QtWidgets.QWidget):

    # The string we will be sending is the file path
    fileClickSgl = QtCore.pyqtSignal(str)

    def __init__(self, startDirectory, parent=None):
        super(FileDialogPane, self).__init__(parent)

        self.currentDirectory = startDirectory

        self.resize(DEFAULT_WIDTH, self.sizeHint().height())

        # Simple vertical stacking of the elements
        self.layout = QtWidgets.QVBoxLayout()

        # Button to change the current directory
        self.dirSelectBtn= QtWidgets.QPushButton("Select Directory")
        self.dirSelectBtn.clicked.connect(self.selectDirectory)

        self.layout.addWidget(self.dirSelectBtn)

        self.currentDirLbl = QtWidgets.QLabel() 
        self.currentDirLbl.setText(self.currentDirectory)
        self.currentDirLbl.setAlignment(Qt.Qt.AlignCenter)
        self.layout.addWidget(self.currentDirLbl)

        # The list of files in the current directory
        self.fileLst = QtWidgets.QListWidget()
        self.fileLst.setSortingEnabled(True)
        self.fileLst.itemActivated.connect(self._onListItemClick)

        self.layout.addWidget(self.fileLst)

        #self.contents = QTextEdit()
        #layout.addWidget(self.contents)
        self.setLayout(self.layout)
        self.setWindowTitle("File Panel")

    def selectDirectory(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory', self.currentDirectory)
        self.currentDirLbl.setText(dirName)
        self.currentDirectory = dirName

        self.updateFileList()


    def updateFileList(self):
        # First, clear the list
        self.fileLst.clear()

        # Now add all of the new items
        fileArr = os.listdir(self.currentDirectory)
        self.fileLst.addItems(fileArr)

    # Decorator indicates that this will be used to signal an event in another widget
    # (in the ImagePane, to be specific)
    @QtCore.pyqtSlot()
    def _onListItemClick(self):
        fileName = self.fileLst.currentItem().text()
        #print(self.currentDirectory + '/' + item.text())
        if len(fileName) > 0:
            self.fileClickSgl.emit(self.currentDirectory + '/' + fileName)
            
		
