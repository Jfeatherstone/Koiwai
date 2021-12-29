import sys
import os

import numpy as np
# Note that there can apparently be an issue with opencv conflicting
# with qt libraries. Make sure that you have them both installed via
# the same package manager (eg. both on pacman or both on pip) so that
# you don't accidently build them separately.
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from UI import EditToolBar

class ImagePane(QtWidgets.QWidget):

    pastDragPosition = None
    
    imageFilePath = None

    activeTool = EditToolBar.POINTER_TOOL

    totalRotation = 0
    totalTranslation = np.array([0, 0], dtype=int)

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
    def setActiveTool(self, toolStr):
        # A couple of the functions have a one-off effect
        if toolStr == EditToolBar.RESET_TOOL:
           
            if self.imageFilePath is not None:
                # Reset the adjustments, and re-render it
                self.setActiveImage(self.imageFilePath)

        else:
            # Otherwise, we just set the active tool to the new one
            self.activeTool = toolStr
            # And update the cursor icon
            self.setCursor(EditToolBar.CURSORS[toolStr])

    @QtCore.pyqtSlot(str)
    def setActiveImage(self, filePath):
        self.imageFilePath = filePath
        self.currentImage = QtGui.QImage(filePath)

        # We may have to adjust the size of the image
        # This will also detect if the image is valid
        self.currentImage = self.fitImageToPane(self.currentImage)

        if self.currentImage != None:

            # We save the image as an array for easy manipulations later on
            # We assume 4 channels
            imgString = self.currentImage.bits().asstring(self.currentImage.width() * self.currentImage.height() * 4)
            self.currentImageArr = np.fromstring(imgString, dtype=np.uint8).reshape((self.currentImage.height(), self.currentImage.width(), 4))

            # The center is also the width/2 or height/2
            self.imageCenter = tuple(np.array(self.currentImageArr.shape[1::-1]) / 2)
        
            self.totalRotation = 0
            self.totalTranslation = np.array([0, 0], dtype=int)

            self.colorBackground.setPixmap(QtGui.QPixmap.fromImage(self.currentImage))
            self.imageCornerPos = self.colorBackground.pos()

    # So that we don't make huge jumps across the screen after you released the mouse button
    def mouseReleaseEvent(self, event):
        self.pastDragPosition = None

    # This is the move drag event, which does different things depending on the current tool
    def mouseMoveEvent(self, event):
        # Keep track of if we have changed the image and need to redisplay it
        editedImage = False

        if self.colorBackground.pixmap() is not None:

            if self.pastDragPosition is not None:

                # Calculate the drag direction
                # event.screenPos() and globalPos() give position relative to screen or window,
                # but just event.pos() gives relative to the image pane (ie. top left corner of the
                posOnImagePane = event.pos()
                differenceVector = posOnImagePane - self.pastDragPosition

                # Now we do different things based on the current tool
                if self.activeTool == EditToolBar.MOVE_TOOL:
                    # image pane is 0, 0)
                    #print(differenceVector)
                    # We don't want to move the image pane itself, but the content
                    self.totalTranslation[0] += differenceVector.x()
                    self.totalTranslation[1] += differenceVector.y()

                    editedImage = True
                
                if self.activeTool == EditToolBar.ROTATE_TOOL:

                    # Determine whether we have a clockwise or counter-clockwise rotation
                    # We always rotate around the center of the image pane
                    center = QtCore.QPoint(self.size().width()*0.5, self.size().height()*0.5)
                    print(center)
                    rotationDir = 0
                    if posOnImagePane.x() > center.x():
                        rotationDir = 2*int(differenceVector.y() > 0) - 1
                    elif posOnImagePane.x() < center.x():
                        rotationDir = 2*int(differenceVector.y() < 0) - 1
            
                    # If the difference vector intersects the vertical line in the center
                    # of the pane, and x is to the right of this line, it is counter-clockwise
                    # The other permutations are reasonably easy to figure out, but the sign of
                    # the quantity intercept * (x > x_center)

                    #if posOnImagePane.x() != center.x():
                    #    slope = (posOnImagePane.y() - center.y()) / (posOnImagePane.x() - center.x())
                    #    intercept = posOnImagePane.y() - slope * posOnImagePane.x()
                    #    
                    #    rotationDir = np.sign(differenceVector.y() * slope * intercept * (posOnImagePane.x() - center.x()))

                    # Scale the angle by the magnitude of the difference vector
                    angle = rotationDir * .1 * np.sqrt(differenceVector.y()**2 + differenceVector.x()**2)

                    # If we just grab the pixmap and rotate, we will lose quality on the image
                    # quite fast, so we re-rotate the original image every time
                    # (probably not the most efficient, but it works)
                    self.totalRotation += angle
                    editedImage = True


            if event.buttons() == QtCore.Qt.LeftButton:
                self.pastDragPosition = event.pos()
            
            # Now update the image and set the pixmap again
            # We apply all of the possible transformations here, since they need to stack

            if editedImage:

                # Angle is in degrees here
                rotationMat = cv2.getRotationMatrix2D(self.imageCenter, self.totalRotation, 1.0)

                # Account for rotation increasing size of the image
                # Note that we only actually increase the size of the image temporarily;
                # in the end, the image (and window) will remain exactly the same size as
                # before, but if we don't increase it for the rotation, we will cut off the
                # corners.
                rotationCos = np.abs(rotationMat[0][0])
                rotationSin = np.abs(rotationMat[0][1])

                newImageHeight = int((2*self.imageCenter[1] * rotationSin) +
                                     (2*self.imageCenter[0] * rotationCos))
                newImageWidth = int((2*self.imageCenter[1] * rotationCos) +
                                    (2*self.imageCenter[0] * rotationSin))

                # Make sure the rotated image is centered in the new frame
                rotationMat[0][2] += (newImageHeight/2) - self.imageCenter[0]
                rotationMat[1][2] += (newImageWidth/2) - self.imageCenter[1]
                newSize = (newImageHeight, newImageWidth)

                # Apply rotation
                result = cv2.warpAffine(self.currentImageArr, rotationMat, newSize)

                # Translation matrix (adjusting for the new center of the frame)
                translationMat = np.float32([[1, 0, self.totalTranslation[0] - (newImageHeight/2 - self.imageCenter[0])],
                                            [0, 1, self.totalTranslation[1] - (newImageWidth/2 - self.imageCenter[1])]])

                # We set the final image size to be exactly the same as before
                finalImageSize = (self.size().height(), self.size().width())

                # Apply translation
                # We crop back to the original size here, so we don't increase the image size
                result = cv2.warpAffine(result, translationMat, self.currentImageArr.shape[1::-1])

                leftCrop = int(result.shape[1]/2 - self.size().width()/2)
                topCrop = int(result.shape[0]/2 - self.size().height()/2)

                
                #result = result[topCrop:topCrop+self.size().height(),leftCrop:leftCrop+self.size().width(),:]

                newImage = Qt.QImage(result, result.shape[1], result.shape[0], Qt.QImage.Format_ARGB32)
                print(newImage.size())
                newImage = self.fitImageToPane(newImage)

                # Now create a new pixmap and display it
                transformedPixmap = QtGui.QPixmap.fromImage(newImage)
                self.colorBackground.setPixmap(transformedPixmap)
