# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DoubleSelectWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DoubleSelectWin(object):
    def setupUi(self, DoubleSelectWin):
        DoubleSelectWin.setObjectName("DoubleSelectWin")
        DoubleSelectWin.resize(568, 494)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        DoubleSelectWin.setFont(font)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(DoubleSelectWin)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_left = QtWidgets.QLabel(DoubleSelectWin)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_left.setFont(font)
        self.label_left.setObjectName("label_left")
        self.verticalLayout.addWidget(self.label_left)
        self.listWidget_left = QtWidgets.QListWidget(DoubleSelectWin)
        self.listWidget_left.setObjectName("listWidget_left")
        self.verticalLayout.addWidget(self.listWidget_left)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(13, 382, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_right = QtWidgets.QLabel(DoubleSelectWin)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_right.setFont(font)
        self.label_right.setObjectName("label_right")
        self.verticalLayout_2.addWidget(self.label_right)
        self.listWidget_right = QtWidgets.QListWidget(DoubleSelectWin)
        self.listWidget_right.setObjectName("listWidget_right")
        self.verticalLayout_2.addWidget(self.listWidget_right)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_ok = QtWidgets.QPushButton(DoubleSelectWin)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(DoubleSelectWin)
        QtCore.QMetaObject.connectSlotsByName(DoubleSelectWin)

    def retranslateUi(self, DoubleSelectWin):
        _translate = QtCore.QCoreApplication.translate
        DoubleSelectWin.setWindowTitle(_translate("DoubleSelectWin", "Select Source and Receiver config files"))
        self.label_left.setText(_translate("DoubleSelectWin", "Select data_1 to display"))
        self.label_right.setText(_translate("DoubleSelectWin", "Select data_2 to display"))
        self.pushButton_ok.setText(_translate("DoubleSelectWin", "OK"))
