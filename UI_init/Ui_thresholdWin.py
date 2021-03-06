# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thresholdWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(516, 185)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSlider_min = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_min.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_min.setObjectName("horizontalSlider_min")
        self.gridLayout.addWidget(self.horizontalSlider_min, 0, 1, 1, 1)
        self.label_min = QtWidgets.QLabel(Dialog)
        self.label_min.setObjectName("label_min")
        self.gridLayout.addWidget(self.label_min, 0, 0, 1, 1)
        self.lineEdit_min = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_min.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_min.setObjectName("lineEdit_min")
        self.gridLayout.addWidget(self.lineEdit_min, 0, 2, 1, 1)
        self.label_max = QtWidgets.QLabel(Dialog)
        self.label_max.setObjectName("label_max")
        self.gridLayout.addWidget(self.label_max, 1, 0, 1, 1)
        self.horizontalSlider_max = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_max.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_max.setObjectName("horizontalSlider_max")
        self.gridLayout.addWidget(self.horizontalSlider_max, 1, 1, 1, 1)
        self.lineEdit_max = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_max.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.gridLayout.addWidget(self.lineEdit_max, 1, 2, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Threshold (Model Cutoff)"))
        self.label.setText(_translate("Dialog", "Enter the max/min cutoff values for the model.If min is grater than max, values between min and max will not be displayed."))
        self.label_min.setText(_translate("Dialog", "min"))
        self.label_max.setText(_translate("Dialog", "max"))
