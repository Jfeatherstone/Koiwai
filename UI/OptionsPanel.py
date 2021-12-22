import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class OptionsPane(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(OptionsPane, self).__init__(parent)

        self.layout = QtWidgets.QHBoxLayout()
        
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
        

        self.layout.addWidget(self.imageManipContainer)


        # Add the various image manipulating items in a little visual container
        self.imageMaskContainer = QtWidgets.QVBoxLayout()
        #self.imageMaskContainer.setStyleSheet("""
        #                                   border: 1px solid black;
        #                                   background-color: blue;
        #                                   """)

        self.imageMaskTitle = QtWidgets.QLabel("Image Mask")
        self.imageMaskTitle.setAlignment(Qt.Qt.AlignCenter)
        self.imageMaskContainer.addWidget(self.imageMaskTitle)

        self.layout.addLayout(self.imageMaskContainer)

        self.setLayout(self.layout)
