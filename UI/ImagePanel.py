import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class ImagePane(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ImagePane, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()

        self.colorBackground = QtWidgets.QLabel()
        self.colorBackground.setAlignment(Qt.Qt.AlignCenter)
        self.colorBackground.setStyleSheet("""
                                           border: 1px solid black;
                                           background-color: gray;
                                           """)
        self.layout.addWidget(self.colorBackground) 
        
        self.setLayout(self.layout)

    @QtCore.pyqtSlot(str)
    def setActiveImage(self, filePath):
        self.colorBackground.setPixmap(QtGui.QPixmap(filePath))
