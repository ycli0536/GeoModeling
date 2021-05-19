from PyQt5.QtWidgets import QDialog, QMessageBox
from UI_init.Ui_SelectWin import Ui_SelectWin

import os

class SelectWin(QDialog, Ui_SelectWin):
    def __init__(self, path, mode):
        super(SelectWin, self).__init__()
        self.setupUi(self)
        self.selecteddir = path
        self.win_type = mode
        self.select_flag = False
        self.label.setText('Select %s to display: ' % self.win_type)
        self.setWindowTitle('Select %s' % self.win_type)

        self.show_dir()
        self.pushButton_ok.clicked.connect(self.get_path)

    def show_dir(self):
        dir = os.listdir(self.selecteddir)
        for i in range(len(dir)):
            self.listWidget.addItem((dir[i]))

    def get_path(self):
        if self.listWidget.selectedItems():
            self.selected_file = self.listWidget.selectedItems()[0].text()
            self.selected_path = os.path.join(self.selecteddir, self.selected_file)
            self.select_flag = True
            self.close()
        else:
            QMessageBox.warning(self, 'Warning', 'You have not select the %s file!' % self.win_type,
                                QMessageBox.Yes)

    def closeEvent(self, event):
        if not self.select_flag:
            reply = QMessageBox.question(self, 'Discard?',
                                         'Discard this operation?',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

