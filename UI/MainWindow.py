import sys
from PyQt5 import QtWidgets, QtCore

from UI import FilePane, ImagePane, OptionsPane	


class MainWindow(QtWidgets.QWidget):

    def __init__(self, app):
        super(MainWindow, self).__init__()

        # Resize the window to fit the screen nicely
        # We give a little bit of padding so you can nicely see everything
        screen = app.primaryScreen()
        defaultWindowSize = screen.size() - QtCore.QSize(50, 75) #(width, height)
        self.resize(defaultWindowSize)

        mainVerticalLayout = QtWidgets.QVBoxLayout()

        # The top options bar that include the various tools you can use to manipulate
        # the images, as well as other utility things
        optionsPane = OptionsPane() 
        mainVerticalLayout.addWidget(optionsPane)
       
        # Technically this isn't actually a layout, but rather widget
        # but we use it exactly as a layout (since splitter automatically
        # puts nice resize handles between objects)
        mainHorizontalLayout = QtWidgets.QSplitter()

        # The left side file pane, that shows the available files you can open
        filePane = FilePane('/home/jack')
        # The central image pane, that displays the current active image
        imagePane = ImagePane()  

        # Take care of communication between the various panels
        filePane.fileClickSgl.connect(imagePane.setActiveImage)

        # Add everything in the proper order
        mainHorizontalLayout.addWidget(filePane)
        mainHorizontalLayout.addWidget(imagePane)
        mainVerticalLayout.addWidget(mainHorizontalLayout)

        self.setLayout(mainVerticalLayout)

        # Set some sizes of objects to make them look good
        imagePane.setMinimumWidth(screen.size().width() - filePane.size().width() - 150)
        optionsPane.setMinimumHeight(120)
        optionsPane.setMaximumHeight(121)

        self.setWindowTitle('Koiwai')
