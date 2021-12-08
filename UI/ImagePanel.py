import sys
import os

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class ImagePane(QtWidgets.QWidget):

    pastDragPosition = None

    totalRotation = 0
    totalTranslation = 0

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
            self.imageCornerPos = self.colorBackground.pos()

    # This is the move drag event, which does different things depending on the current tool
    def mouseMoveEvent(self, event):
        moveTool = False
        rotateTool = True


        if self.colorBackground.pixmap() is not None:

            if self.pastDragPosition is not None:

                # Calculate the drag direction
                # event.screenPos() and globalPos() give position relative to screen or window,
                # but just event.pos() gives relative to the image pane (ie. top left corner of the
                posOnImagePane = event.pos()
                differenceVector = posOnImagePane - self.pastDragPosition

                # Now we do different things based on the current tool
                if moveTool:
                    print("move")
                    # image pane is 0, 0)
                    #print(differenceVector)
                    # We don't want to move the image pane itself, but the content
                    translate = QtGui.QTransform().translate(differenceVector.x(), differenceVector.y())
                    self.colorBackground.setPixmap(self.colorBackground.pixmap().transformed(translate, QtCore.Qt.SmoothTransformation))
                    print(self.colorBackground.pixmap())
                    #if event.buttons() == QtCore.Qt.LeftButton:
                    #    print("left button")
                
                if rotateTool:
                    print("rotate")

                    # Determine whether we have a clockwise or counter-clockwise rotation
                    # We always rotate around the center of the image pane
                    center = QtCore.QPoint(self.size().width()*0.5, self.size().height()*0.5)
                    print(center)
                    rotationDir = 0
                    if posOnImagePane.x() > center.x():
                        rotationDir = 2*int(differenceVector.y() > 0) - 1
                    elif posOnImagePane.x() < center.x():
                        rotationDir = 2*int(differenceVector.y() < 0) - 1
                    
                    # Scale the angle by the magnitude of the difference vector
                    angle = rotationDir * .1 * np.sqrt(differenceVector.y()**2 + differenceVector.x()**2)

                    # If we just grab the pixmap and rotate, we will lose quality on the image
                    # quite fast, so we re-rotate the original image every time
                    # (probably not the most efficient, but it works)
                    self.totalRotation += angle
                    transform = QtGui.QTransform()
                    transform.rotate(self.totalRotation)
                    transformedPixmap = QtGui.QPixmap.fromImage(self.currentImage).transformed(transform, QtCore.Qt.SmoothTransformation)
                    self.colorBackground.setPixmap(transformedPixmap)


            self.pastDragPosition = event.pos()
