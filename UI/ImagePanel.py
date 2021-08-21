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

    def fitImageToPane(self, image: QtGui.QImage):

        # The 1.02 makes sure that the window doesn't get larger because of rounding errors
        widthRatio = image.size().width() / self.colorBackground.size().width() * 1.02
        heightRatio = image.size().height() / self.colorBackground.size().height() * 1.02

        # This indicates the image is not a proper image
        if widthRatio == 0 and heightRatio == 0:
            return None

        if widthRatio > 1 and heightRatio > 1:
            return image.scaled(self.currentImage.size() / max(widthRatio, heightRatio))
        elif widthRatio > 1:
            return image.scaled(self.currentImage.size() / widthRatio)
        elif heightRatio > 1:
            return image.scaled(self.currentImage.size() / heightRatio)
        else:
            return image


    @QtCore.pyqtSlot(str)
    def setActiveImage(self, filePath):
        self.currentImage = QtGui.QImage(filePath)

        # We may have to adjust the size of the image
        # This will also detect if the image is valid
        self.currentImage = self.fitImageToPane(self.currentImage)

        if self.currentImage != None:

            self.colorBackground.setPixmap(QtGui.QPixmap.fromImage(self.currentImage))
