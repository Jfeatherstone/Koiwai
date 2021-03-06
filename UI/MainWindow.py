import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from UI import FilePane, ImagePane, OptionsPane, EditToolBar


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        """
        General window settings
        -----------------------
        """
       
        # Resize the window to fit the screen nicely
        # We give a little bit of padding so you can nicely see everything
        screen = app.primaryScreen()
        defaultWindowSize = screen.size() - QtCore.QSize(50, 75) #(width, height)
        self.resize(defaultWindowSize)


        """
        Menu bar
        --------
        """

        self.menuBar = QtWidgets.QMenuBar()
        self.setMenuBar(self.menuBar)

        self.fileMenu = self.menuBar.addMenu("File")
        self.editMenu = self.menuBar.addMenu("Edit")
        self.helpMenu = self.menuBar.addMenu("Help")

        """
        Tool bars
        --------
        """
        # Basic file operations
        self.fileToolBar = self.addToolBar('File')

        self.saveTool = QtWidgets.QAction(QtGui.QIcon(':save'), '&Save')
        self.exportTool = QtWidgets.QAction(QtGui.QIcon(':printer'), '&Export')
        self.previousImageTool = QtWidgets.QAction(QtGui.QIcon(':skip-back'), '&Previous Image')
        self.nextImageTool = QtWidgets.QAction(QtGui.QIcon(':skip-forward'), '&Next Image')

        self.fileToolBar.addAction(self.saveTool)
        self.fileToolBar.addAction(self.exportTool)
        self.fileToolBar.addAction(self.previousImageTool)
        self.fileToolBar.addAction(self.nextImageTool)

        # The various image manipulation tools

        self.editToolBar = EditToolBar.EditToolBar()
        self.addToolBar(self.editToolBar)
        #self.editToolBar = self.addToolBar('Edit')
        """
        Main window content
        -------------------
        """

        self.centralWidget = QtWidgets.QWidget()

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

        self.editToolBar.toolClickSgl.connect(imagePane.setActiveTool)

        # Add everything in the proper order
        mainHorizontalLayout.addWidget(filePane)
        mainHorizontalLayout.addWidget(imagePane)
        mainVerticalLayout.addWidget(mainHorizontalLayout)

        self.centralWidget.setLayout(mainVerticalLayout)
        self.setCentralWidget(self.centralWidget)

        # Set some sizes of objects to make them look good
        imagePane.setMinimumWidth(screen.size().width() - filePane.size().width() - 150)
        optionsPane.setMinimumHeight(120)
        optionsPane.setMaximumHeight(121)


        self.setWindowTitle('Koiwai')
