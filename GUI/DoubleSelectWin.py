from PyQt5.QtWidgets import QDialog, QMessageBox
from UI_init.Ui_DoubleSelectWin import Ui_DoubleSelectWin

import os


class DoubleSelectWin(QDialog, Ui_DoubleSelectWin):
    def __init__(self, paths, modes):
        super(DoubleSelectWin, self).__init__()
        self.setupUi(self)
        self.selecteddirs = paths
        self.win_types = modes
        self.select_flag = False
        self.label_left.setText('Select %s to display: ' % self.win_types[0])
        self.label_right.setText('Select %s to display: ' % self.win_types[1])
        self.setWindowTitle('Select %s and %s files' % (self.win_types[0], self.win_types[1]))

        self.show_dirs()
        self.pushButton_ok.clicked.connect(self.get_paths)

    def show_dirs(self):
        dir_left = os.listdir(self.selecteddirs[0])
        self.listWidget_left.addItems(dir_left)
        dir_right = os.listdir(self.selecteddirs[1])
        self.listWidget_right.addItems(dir_right)

    def get_paths(self):
        if self.listWidget_left.selectedItems() and self.listWidget_right.selectedItems():
            self.selected_file_left = self.listWidget_left.selectedItems()[0].text()
            self.selected_path_left = os.path.join(self.selecteddirs[0], self.selected_file_left)
            self.selected_file_right = self.listWidget_right.selectedItems()[0].text()
            self.selected_path_right = os.path.join(self.selecteddirs[1], self.selected_file_right)
            self.select_flag = True
            self.close()
        else:
            QMessageBox.warning(self, 'Warning',
                                'You have not select all the %s and %s files!' % (self.win_types[0], self.win_types[1]),
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

