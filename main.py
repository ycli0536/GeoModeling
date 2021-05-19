from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from GUI.MainWin import FracMainWindow as MainWindow


if __name__ == '__main__':
    app = QApplication([])
    # app.setWindowIcon(QtGui.QIcon('UI/image.png'))

    mainWindow = MainWindow()

    mainWindow.show()
    app.exec_()
