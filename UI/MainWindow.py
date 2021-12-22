import sys
from PyQt5 import QtWidgets, QtCore, QtGui

from UI import FilePane, ImagePane, OptionsPane	


class MainWindow(QtWidgets.QMainWindow):

    moveToolClickSgl = QtCore.pyqtSignal(str)

    def _clickMove(self, event):
        #moveToolClickSgl.emit()
        pass

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
        self.editToolBar = self.addToolBar('Edit')

        self.moveTool = QtWidgets.QAction(QtGui.QIcon(':move'), '&Move')
        self.cutTool = QtWidgets.QAction(QtGui.QIcon(':scissors'), '&Cut')
        self.undoTool = QtWidgets.QAction(QtGui.QIcon(':undo'), '&Undo')
        self.resetViewTool = QtWidgets.QAction(QtGui.QIcon(':square'), '&Reset View')
        self.zoomInTool = QtWidgets.QAction(QtGui.QIcon(':maximize'), '&Zoom In')
        self.zoomOutTool = QtWidgets.QAction(QtGui.QIcon(':minimize'), '&Zoom Out')

        self.editToolBar.addAction(self.moveTool)
        self.editToolBar.addAction(self.undoTool)
        self.editToolBar.addAction(self.cutTool)
        self.editToolBar.addAction(self.resetViewTool)
        self.editToolBar.addAction(self.zoomInTool)
        self.editToolBar.addAction(self.zoomOutTool)

        self.moveTool.triggered.connect(self._clickMove)
    
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
