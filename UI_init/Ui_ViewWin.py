# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ViewWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(978, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commandLinkButton_mesh = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton_mesh.setObjectName("commandLinkButton_mesh")
        self.horizontalLayout.addWidget(self.commandLinkButton_mesh)
        self.label_MeshPath = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_MeshPath.setFont(font)
        self.label_MeshPath.setText("")
        self.label_MeshPath.setWordWrap(True)
        self.label_MeshPath.setObjectName("label_MeshPath")
        self.horizontalLayout.addWidget(self.label_MeshPath)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.commandLinkButton_model = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton_model.setObjectName("commandLinkButton_model")
        self.horizontalLayout.addWidget(self.commandLinkButton_model)
        self.label_ModelPath = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_ModelPath.setFont(font)
        self.label_ModelPath.setText("")
        self.label_ModelPath.setWordWrap(True)
        self.label_ModelPath.setObjectName("label_ModelPath")
        self.horizontalLayout.addWidget(self.label_ModelPath)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 978, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menu_Bounds = QtWidgets.QMenu(self.menuView)
        self.menu_Bounds.setObjectName("menu_Bounds")
        self.menu_Scalars = QtWidgets.QMenu(self.menuView)
        self.menu_Scalars.setObjectName("menu_Scalars")
        self.menu_Display = QtWidgets.QMenu(self.menuView)
        self.menu_Display.setObjectName("menu_Display")
        self.menu_Ticks = QtWidgets.QMenu(self.menuView)
        self.menu_Ticks.setObjectName("menu_Ticks")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuEditor = QtWidgets.QMenu(self.menubar)
        self.menuEditor.setObjectName("menuEditor")
        self.menuAdd = QtWidgets.QMenu(self.menubar)
        self.menuAdd.setObjectName("menuAdd")
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
        self.action_Crop = QtWidgets.QAction(MainWindow)
        self.action_Crop.setObjectName("action_Crop")
        self.action_log = QtWidgets.QAction(MainWindow)
        self.action_log.setObjectName("action_log")
        self.action_normal = QtWidgets.QAction(MainWindow)
        self.action_normal.setObjectName("action_normal")
        self.action_AddPoints = QtWidgets.QAction(MainWindow)
        self.action_AddPoints.setObjectName("action_AddPoints")
        self.action_PyVista = QtWidgets.QAction(MainWindow)
        self.action_PyVista.setObjectName("action_PyVista")
        self.action_UBC = QtWidgets.QAction(MainWindow)
        self.action_UBC.setObjectName("action_UBC")
        self.action_AddLines = QtWidgets.QAction(MainWindow)
        self.action_AddLines.setObjectName("action_AddLines")
        self.action_LocalMesh = QtWidgets.QAction(MainWindow)
        self.action_LocalMesh.setObjectName("action_LocalMesh")
        self.action_RealMesh = QtWidgets.QAction(MainWindow)
        self.action_RealMesh.setObjectName("action_RealMesh")
        self.action_ReverseXY = QtWidgets.QAction(MainWindow)
        self.action_ReverseXY.setObjectName("action_ReverseXY")
        self.action_Add = QtWidgets.QAction(MainWindow)
        self.action_Add.setObjectName("action_Add")
        self.action_SaveScreenshot = QtWidgets.QAction(MainWindow)
        self.action_SaveScreenshot.setObjectName("action_SaveScreenshot")
        self.menuFile.addAction(self.action_Load)
        self.menuFile.addAction(self.action_Add)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_SaveScreenshot)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Exit)
        self.menu_Bounds.addAction(self.action_BoundingBox)
        self.menu_Bounds.addAction(self.action_Bounds)
        self.menu_Scalars.addAction(self.action_log)
        self.menu_Scalars.addAction(self.action_normal)
        self.menu_Display.addAction(self.action_PyVista)
        self.menu_Display.addAction(self.action_UBC)
        self.menu_Ticks.addAction(self.action_LocalMesh)
        self.menu_Ticks.addAction(self.action_RealMesh)
        self.menuView.addAction(self.menu_Display.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Wireframe)
        self.menuView.addAction(self.menu_Bounds.menuAction())
        self.menuView.addAction(self.menu_Ticks.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.menu_Scalars.menuAction())
        self.menuView.addAction(self.action_Orientation_Marker)
        self.menuView.addAction(self.action_ReverseXY)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Camera)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Clear)
        self.menuTools.addAction(self.action_Threshold)
        self.menuTools.addAction(self.action_Crop)
        self.menuAdd.addAction(self.action_AddPoints)
        self.menuAdd.addAction(self.action_AddLines)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuEditor.menuAction())
        self.menubar.addAction(self.menuAdd.menuAction())
        self.toolBar.addAction(self.action_XOZview)
        self.toolBar.addAction(self.action_XOYview)
        self.toolBar.addAction(self.action_YOZview)
        self.toolBar.addAction(self.action_Isometric)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Bounds)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_PyVista)
        self.toolBar.addAction(self.action_UBC)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_log)
        self.toolBar.addAction(self.action_normal)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Threshold)
        self.toolBar.addAction(self.action_Crop)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "View model"))
        self.commandLinkButton_mesh.setText(_translate("MainWindow", "Mesh file:"))
        self.commandLinkButton_model.setText(_translate("MainWindow", "Model file:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menu_Bounds.setTitle(_translate("MainWindow", "Bounds"))
        self.menu_Scalars.setTitle(_translate("MainWindow", "Scalars"))
        self.menu_Display.setTitle(_translate("MainWindow", "Display Format"))
        self.menu_Ticks.setTitle(_translate("MainWindow", "Ticks"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuEditor.setTitle(_translate("MainWindow", "Editor"))
        self.menuAdd.setTitle(_translate("MainWindow", "Add"))
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
        self.action_Crop.setText(_translate("MainWindow", "Crop"))
        self.action_log.setText(_translate("MainWindow", "log"))
        self.action_normal.setText(_translate("MainWindow", "normal"))
        self.action_AddPoints.setText(_translate("MainWindow", "Points"))
        self.action_PyVista.setText(_translate("MainWindow", "PyVista"))
        self.action_UBC.setText(_translate("MainWindow", "UBC"))
        self.action_AddLines.setText(_translate("MainWindow", "Lines"))
        self.action_LocalMesh.setText(_translate("MainWindow", "Local mesh"))
        self.action_RealMesh.setText(_translate("MainWindow", "Real mesh"))
        self.action_ReverseXY.setText(_translate("MainWindow", "Reverse XY"))
        self.action_Add.setText(_translate("MainWindow", "Add"))
        self.action_SaveScreenshot.setText(_translate("MainWindow", "Save Screenshot"))
