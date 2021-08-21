import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets

class OptionsPane(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(OptionsPane, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.colorBackground = QtWidgets.QWidget()
        self.colorBackground.setStyleSheet("""
                                           border: 1px solid black;
                                           background-color: #AAAAAA;
                                           """)
        self.layout.addWidget(self.colorBackground)
       
        # Add the various image manipulating items in a little visual container
        self.imageManipContainer = QtWidgets.QLabel()
        self.imageManipContainer.setStyleSheet("""
                                           border: 1px solid black;
                                           background-color: red;
                                           """)
        

        #self.colorBackground.addWidget(self.imageManipContainer)

        self.setLayout(self.layout)
