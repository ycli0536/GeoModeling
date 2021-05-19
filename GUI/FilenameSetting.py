from PyQt5.QtWidgets import QDialog, QMessageBox, QCheckBox

from UI_init.Ui_FileNameSetting import Ui_Dialog as Ui_FileNameSetting


class FileNameSettingWin(Ui_FileNameSetting, QDialog):
    def __init__(self):
        super(FileNameSettingWin, self).__init__()
        self.setupUi(self)
        self.create_flag = False

        self.pushButton_save.clicked.connect(self.ok)

    def multi_save_category(self):
        self.checkBox_1 = QCheckBox('rcv paths')
        self.checkBox_2 = QCheckBox('observed points')
        self.horizontalLayout_btm.insertWidget(self.checkBox_2, 0)
        self.horizontalLayout_btm.insertWidget(self.checkBox_1, 0)

    def ok(self):
        if not self.lineEdit_filename.text():
            QMessageBox.warning(self, 'Warning', 'You have not declare the filename!',
                                QMessageBox.Yes)
        else:
            self.create_flag = True
            self.close()

    def closeEvent(self, event):
        if not self.create_flag:
            reply = QMessageBox.question(self, 'Information',
                                         'Discard this save?',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
