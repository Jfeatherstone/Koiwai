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

    mainHorizontalLayout = QtWidgets.QHBoxLayout()

    filePane = FileDialogPane('/home/jack')
    imagePane = ImagePane()  
    optionsPane = OptionsPane()

    # Take care of communication between the various panels
    filePane.fileClickSgl.connect(imagePane.setActiveImage)

    # Add everything in the proper order
    mainVerticalLayout.addWidget(optionsPane)

    mainHorizontalLayout.addWidget(filePane)
    mainHorizontalLayout.addWidget(imagePane)
    mainVerticalLayout.addLayout(mainHorizontalLayout)

    mainWindowWidget.setLayout(mainVerticalLayout)

    # Set some sizes of objects to make them look good
    imagePane.setMinimumSize(screen.size().width() - filePane.size().width() - 100, -1)
    optionsPane.setMinimumSize(-1, 120)

    mainWindowWidget.setWindowTitle('Koiwai')
    mainWindowWidget.show() 


    sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
