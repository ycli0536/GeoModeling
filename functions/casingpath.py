from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QMessageBox
from PyQt5 import QtCore, QtGui

from UI_wellpathSetting import Ui_Dialog
from wellpath2edge import wellpath2edge

from TabClass import addModelName
from selectWin import SelectWin

import os
import numpy as np


class WellpathSettingDialog(QDialog, Ui_Dialog):
    def __init__(self, path):
        super(WellpathSettingDialog, self).__init__()
        self.setupUi(self)
        self.path = path

        self.tableWidget.setColumnCount(3)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(("X"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(("Y"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(("Z"))

        self.lineEdit_pN.editingFinished.connect(self.tableset)
        self.pushBtn_Mesh.clicked.connect(self.LoadMesh)
        self.buttonBox.accepted.connect(self.CasingSetting)

    def tableset(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(("X"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(("Y"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(("Z"))

        try:
            Row=int(self.lineEdit_pN.text())
            self.tableWidget.setRowCount(Row)
            self.Push=[0]*(Row-1)
            for i in range(Row):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
                self.tableWidget.verticalHeader().setDefaultSectionSize(30)
                self.tableWidget.verticalHeader().setMinimumSectionSize(20)
                self.tableWidget.verticalHeaderItem(i).setText((str(i+1)))

                item = QTableWidgetItem()

                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPixelSize(15)
                item.setFont(font)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 0, item)
                item = QTableWidgetItem()
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPixelSize(15)
                item.setFont(font)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 1, item)
                item = QTableWidgetItem()
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPixelSize(15)
                item.setFont(font)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 2, item)
        except ValueError:
            pass

    def LoadMesh(self):
        win = SelectWin(os.path.join(self.path, 'Mesh'), 'mesh')
        if win.exec() == 1:
            with open(win.selectedpath, 'r') as f:
                ff = f.readlines()
                sp = ff[0].split()
                nodeX = np.array(sp)
                sp = ff[1].split()
                nodeY = np.array(sp)
                sp = ff[2].split()
                nodeZ = np.array(sp)
            nodeX = nodeX.astype(float)
            nodeY = nodeY.astype(float)
            nodeZ = nodeZ.astype(float)

            self.nodeX = nodeX.astype(float)
            self.nodeY = nodeY.astype(float)
            self.nodeZ = nodeZ.astype(float)

    def showName(self):
        namewin = addModelName()
        def getname():
            self.wellpathName = namewin.lineEdit.text()
            self.wellpathName = "edgeCon_" + self.wellpathName + ".txt"

        namewin.lineEdit.textChanged.connect(getname)
        namewin.pushButton.clicked.connect(namewin.close)
        namewin.exec()

    def CasingSetting(self):
        try:
            wellpath_ctrlPoints = np.empty(shape=(self.tableWidget.rowCount(), 3))
            for i in range(self.tableWidget.rowCount()):
                wellpath_ctrlPoints[i][0] = float(self.tableWidget.item(i, 0).text())
                wellpath_ctrlPoints[i][1] = float(self.tableWidget.item(i, 1).text())
                wellpath_ctrlPoints[i][2] = float(self.tableWidget.item(i, 2).text())

            d = float(self.lineEdit_int.text())
            wellpath_discrete = []
            for i in range(wellpath_ctrlPoints.shape[0] - 1):
                dx = (wellpath_ctrlPoints[i + 1][0] - wellpath_ctrlPoints[i][0])
                dy = (wellpath_ctrlPoints[i + 1][1] - wellpath_ctrlPoints[i][1])
                dz = (wellpath_ctrlPoints[i + 1][2] - wellpath_ctrlPoints[i][2])
                length = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
                n = np.ceil(length / d)
                for j in range(int(n)):
                    wellpath_discrete.append([wellpath_ctrlPoints[i][0] + j * d * (dx / length),
                                              wellpath_ctrlPoints[i][1] + j * d * (dy / length),
                                              wellpath_ctrlPoints[i][2] + j * d * (dz / length)])
                wellpath_discrete.append([wellpath_ctrlPoints[i + 1][0] - (length % d) * (dx / length),
                                          wellpath_ctrlPoints[i + 1][1] - (length % d) * (dy / length),
                                          wellpath_ctrlPoints[i + 1][2] - (length % d) * (dz / length)])

            self.edgeCon = wellpath2edge(nodeX=self.nodeX, nodeY=self.nodeY, nodeZ=self.nodeZ,
                                         wellpath=np.array(wellpath_discrete), wellCon=float(self.lineEdit_edgeCon.text()))
            # print(np.where(self.edgeCon != 0))

            self.showName()
            wellpathPath = os.path.join(self.path, *["Background", self.wellpathName])
            if wellpathPath == "":
                return
            else:
                np.savetxt(wellpathPath, self.edgeCon)
        except AttributeError:
            QMessageBox.warning(self.buttonBox,
                                "Error",
                                "Please fill all necessary parameters!",
                                QMessageBox.Yes)
        except ValueError:
            QMessageBox.warning(self.buttonBox,
                                "Error",
                                "Please fill approved edgeCon value!",
                                QMessageBox.Yes)
