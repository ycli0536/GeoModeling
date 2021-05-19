# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ViewWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menu_Bounds = QtWidgets.QMenu(self.menuView)
        self.menu_Bounds.setObjectName("menu_Bounds")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuEditor = QtWidgets.QMenu(self.menubar)
        self.menuEditor.setObjectName("menuEditor")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Clear = QtWidgets.QAction(MainWindow)
        self.action_Clear.setObjectName("action_Clear")
        self.action_Camera = QtWidgets.QAction(MainWindow)
        self.action_Camera.setObjectName("action_Camera")
        self.action_XOZview = QtWidgets.QAction(MainWindow)
        self.action_XOZview.setObjectName("action_XOZview")
        self.action_XOYview = QtWidgets.QAction(MainWindow)
        self.action_XOYview.setObjectName("action_XOYview")
        self.action_YOZview = QtWidgets.QAction(MainWindow)
        self.action_YOZview.setObjectName("action_YOZview")
        self.action_Isometric = QtWidgets.QAction(MainWindow)
        self.action_Isometric.setObjectName("action_Isometric")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Threshold = QtWidgets.QAction(MainWindow)
        self.action_Threshold.setObjectName("action_Threshold")
        self.action_Wireframe = QtWidgets.QAction(MainWindow)
        self.action_Wireframe.setObjectName("action_Wireframe")
        self.action_BoundingBox = QtWidgets.QAction(MainWindow)
        self.action_BoundingBox.setObjectName("action_BoundingBox")
        self.action_Bounds = QtWidgets.QAction(MainWindow)
        self.action_Bounds.setObjectName("action_Bounds")
        self.action_Orientation_Marker = QtWidgets.QAction(MainWindow)
        self.action_Orientation_Marker.setObjectName("action_Orientation_Marker")
        self.action_Load = QtWidgets.QAction(MainWindow)
        self.action_Load.setObjectName("action_Load")
        self.menuFile.addAction(self.action_Load)
        self.menuFile.addAction(self.action_Exit)
        self.menu_Bounds.addAction(self.action_BoundingBox)
        self.menu_Bounds.addAction(self.action_Bounds)
        self.menuView.addAction(self.action_Wireframe)
        self.menuView.addAction(self.menu_Bounds.menuAction())
        self.menuView.addAction(self.action_Orientation_Marker)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Camera)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Clear)
        self.menuTools.addAction(self.action_Threshold)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuEditor.menuAction())
        self.toolBar.addAction(self.action_XOZview)
        self.toolBar.addAction(self.action_XOYview)
        self.toolBar.addAction(self.action_YOZview)
        self.toolBar.addAction(self.action_Wireframe)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Isometric)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "View model"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menu_Bounds.setTitle(_translate("MainWindow", "Bounds"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuEditor.setTitle(_translate("MainWindow", "Editor"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_Clear.setText(_translate("MainWindow", "Clear All"))
        self.action_Camera.setText(_translate("MainWindow", "Camera"))
        self.action_XOZview.setText(_translate("MainWindow", "XOZ view"))
        self.action_XOYview.setText(_translate("MainWindow", "XOY view"))
        self.action_XOYview.setToolTip(_translate("MainWindow", "XOY view"))
        self.action_YOZview.setText(_translate("MainWindow", "YOZ view"))
        self.action_YOZview.setToolTip(_translate("MainWindow", "YOZ view"))
        self.action_Isometric.setText(_translate("MainWindow", "Isometric"))
        self.action_Isometric.setToolTip(_translate("MainWindow", "Isometric"))
        self.action_Exit.setText(_translate("MainWindow", "Exit"))
        self.action_Exit.setShortcut(_translate("MainWindow", "Esc"))
        self.action_Threshold.setText(_translate("MainWindow", "Threshold"))
        self.action_Wireframe.setText(_translate("MainWindow", "Wireframe"))
        self.action_Wireframe.setToolTip(_translate("MainWindow", "Wireframe"))
        self.action_BoundingBox.setText(_translate("MainWindow", "Bounding box"))
        self.action_Bounds.setText(_translate("MainWindow", "Bounds"))
        self.action_Orientation_Marker.setText(_translate("MainWindow", "Orientation Marker"))
        self.action_Load.setText(_translate("MainWindow", "Load"))
