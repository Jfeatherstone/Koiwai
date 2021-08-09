import sys
from PyQt5 import QtWidgets

from FilePanel import FileDialogPane
from ImagePanel import ImagePane
from OptionsPanel import OptionsPane

def main():
   
    # The overall app (note this includes all currently active windows)
    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()

    # The overall layout for the main window
    mainWindowWidget = QtWidgets.QWidget()
    mainWindowWidget.resize(screen.size())
    mainVerticalLayout = QtWidgets.QVBoxLayout()

    optionsPane = OptionsPane() 
    mainVerticalLayout.addWidget(optionsPane)
   
    # Technically this isn't actually a layout, but rather widget
    # but we use it exactly as a layout (since splitter automatically
    # puts nice resize handles between objects)
    mainHorizontalLayout = QtWidgets.QSplitter()

    filePane = FileDialogPane('/home/jack')
    imagePane = ImagePane()  

    # Take care of communication between the various panels
    filePane.fileClickSgl.connect(imagePane.setActiveImage)

    # Add everything in the proper order

    mainHorizontalLayout.addWidget(filePane)
    mainHorizontalLayout.addWidget(imagePane)
    mainVerticalLayout.addWidget(mainHorizontalLayout)

    mainWindowWidget.setLayout(mainVerticalLayout)

    # Set some sizes of objects to make them look good
    imagePane.setMinimumWidth(screen.size().width() - filePane.size().width() - 150)
    optionsPane.setMinimumHeight(120)
    optionsPane.setMaximumHeight(121)

    mainWindowWidget.setWindowTitle('Koiwai')
    mainWindowWidget.show() 


    sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
