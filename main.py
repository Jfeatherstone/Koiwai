import sys
from PyQt5 import QtWidgets

from UI.MainWindow import MainWindow

if __name__ == '__main__':
 
    # Create the application
    # Note that this includes all active windows, not just the main one
    app = QtWidgets.QApplication(sys.argv)

    # Now the main window
    window = MainWindow(app)
    # And show it
    window.show()
    
    # Run the application
    sys.exit(app.exec())
