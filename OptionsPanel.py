import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets

class OptionsPane(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(OptionsPane, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()

        self.colorBackground = QtWidgets.QLabel()
        self.colorBackground.setStyleSheet("""
                                           border: 1px solid black;
                                           background-color: red;
                                           """)
        self.layout.addWidget(self.colorBackground)
        
        self.setLayout(self.layout)
