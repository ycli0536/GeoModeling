# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1376, 834)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.treeView = QtWidgets.QTreeView(self.splitter)
        self.treeView.setObjectName("treeView")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(261, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1376, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Mesh = QtWidgets.QMenu(self.menubar)
        self.menu_Mesh.setObjectName("menu_Mesh")
        self.menu_Background = QtWidgets.QMenu(self.menubar)
        self.menu_Background.setObjectName("menu_Background")
        self.menu_WellPath = QtWidgets.QMenu(self.menu_Background)
        self.menu_WellPath.setObjectName("menu_WellPath")
        self.menu_SurveyDesign = QtWidgets.QMenu(self.menubar)
        self.menu_SurveyDesign.setObjectName("menu_SurveyDesign")
        self.menu_ImportConfig = QtWidgets.QMenu(self.menu_SurveyDesign)
        self.menu_ImportConfig.setObjectName("menu_ImportConfig")
        self.menuView = QtWidgets.QMenu(self.menu_SurveyDesign)
        self.menuView.setObjectName("menuView")
        self.menu_ModelGen = QtWidgets.QMenu(self.menubar)
        self.menu_ModelGen.setObjectName("menu_ModelGen")
        self.menu_SlabGen = QtWidgets.QMenu(self.menu_ModelGen)
        self.menu_SlabGen.setObjectName("menu_SlabGen")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_NewProject = QtWidgets.QAction(MainWindow)
        self.action_NewProject.setObjectName("action_NewProject")
        self.action_OpenProject = QtWidgets.QAction(MainWindow)
        self.action_OpenProject.setObjectName("action_OpenProject")
        self.action_Export = QtWidgets.QAction(MainWindow)
        self.action_Export.setObjectName("action_Export")
        self.action_CropModels = QtWidgets.QAction(MainWindow)
        self.action_CropModels.setObjectName("action_CropModels")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.action_NewMesh = QtWidgets.QAction(MainWindow)
        self.action_NewMesh.setObjectName("action_NewMesh")
        self.action_ImportMesh = QtWidgets.QAction(MainWindow)
        self.action_ImportMesh.setObjectName("action_ImportMesh")
        self.action_ViewMesh = QtWidgets.QAction(MainWindow)
        self.action_ViewMesh.setObjectName("action_ViewMesh")
        self.action_SaveMesh = QtWidgets.QAction(MainWindow)
        self.action_SaveMesh.setObjectName("action_SaveMesh")
        self.action_NewBkg = QtWidgets.QAction(MainWindow)
        self.action_NewBkg.setObjectName("action_NewBkg")
        self.action_AddSlab = QtWidgets.QAction(MainWindow)
        self.action_AddSlab.setObjectName("action_AddSlab")
        self.action_AddEllipsoid = QtWidgets.QAction(MainWindow)
        self.action_AddEllipsoid.setObjectName("action_AddEllipsoid")
        self.action_ViewBkg = QtWidgets.QAction(MainWindow)
        self.action_ViewBkg.setObjectName("action_ViewBkg")
        self.action_NewSurvey = QtWidgets.QAction(MainWindow)
        self.action_NewSurvey.setObjectName("action_NewSurvey")
        self.action_ImportSrc = QtWidgets.QAction(MainWindow)
        self.action_ImportSrc.setObjectName("action_ImportSrc")
        self.action_ImportRcv = QtWidgets.QAction(MainWindow)
        self.action_ImportRcv.setObjectName("action_ImportRcv")
        self.action_EllipsoidGen = QtWidgets.QAction(MainWindow)
        self.action_EllipsoidGen.setObjectName("action_EllipsoidGen")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.action_Guide = QtWidgets.QAction(MainWindow)
        self.action_Guide.setObjectName("action_Guide")
        self.action_DesignWellPath = QtWidgets.QAction(MainWindow)
        self.action_DesignWellPath.setObjectName("action_DesignWellPath")
        self.action_ImportWellPath = QtWidgets.QAction(MainWindow)
        self.action_ImportWellPath.setObjectName("action_ImportWellPath")
        self.action_ViewSurvey = QtWidgets.QAction(MainWindow)
        self.action_ViewSurvey.setObjectName("action_ViewSurvey")
        self.action_View_added_well_paths = QtWidgets.QAction(MainWindow)
        self.action_View_added_well_paths.setObjectName("action_View_added_well_paths")
        self.action_ViewModels = QtWidgets.QAction(MainWindow)
        self.action_ViewModels.setObjectName("action_ViewModels")
        self.action_RectangularSlab = QtWidgets.QAction(MainWindow)
        self.action_RectangularSlab.setObjectName("action_RectangularSlab")
        self.action_OctagonalSlab = QtWidgets.QAction(MainWindow)
        self.action_OctagonalSlab.setObjectName("action_OctagonalSlab")
        self.action_DiskSlab = QtWidgets.QAction(MainWindow)
        self.action_DiskSlab.setObjectName("action_DiskSlab")
        self.menu_File.addAction(self.action_NewProject)
        self.menu_File.addAction(self.action_OpenProject)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Export)
        self.menu_File.addAction(self.action_CropModels)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_ViewModels)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menu_Mesh.addAction(self.action_NewMesh)
        self.menu_Mesh.addAction(self.action_ImportMesh)
        self.menu_Mesh.addAction(self.action_ViewMesh)
        self.menu_Mesh.addSeparator()
        self.menu_Mesh.addAction(self.action_SaveMesh)
        self.menu_WellPath.addAction(self.action_ImportWellPath)
        self.menu_Background.addAction(self.action_NewBkg)
        self.menu_Background.addSeparator()
        self.menu_Background.addAction(self.menu_WellPath.menuAction())
        self.menu_Background.addSeparator()
        self.menu_Background.addAction(self.action_AddSlab)
        self.menu_Background.addAction(self.action_AddEllipsoid)
        self.menu_Background.addSeparator()
        self.menu_Background.addAction(self.action_ViewBkg)
        self.menu_ImportConfig.addAction(self.action_ImportSrc)
        self.menu_ImportConfig.addAction(self.action_ImportRcv)
        self.menuView.addAction(self.action_ViewSurvey)
        self.menuView.addAction(self.action_View_added_well_paths)
        self.menu_SurveyDesign.addAction(self.action_NewSurvey)
        self.menu_SurveyDesign.addAction(self.menu_ImportConfig.menuAction())
        self.menu_SurveyDesign.addSeparator()
        self.menu_SurveyDesign.addAction(self.menuView.menuAction())
        self.menu_SlabGen.addAction(self.action_DiskSlab)
        self.menu_SlabGen.addAction(self.action_RectangularSlab)
        self.menu_SlabGen.addAction(self.action_OctagonalSlab)
        self.menu_ModelGen.addAction(self.menu_SlabGen.menuAction())
        self.menu_ModelGen.addAction(self.action_EllipsoidGen)
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.action_Guide)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Mesh.menuAction())
        self.menubar.addAction(self.menu_Background.menuAction())
        self.menubar.addAction(self.menu_SurveyDesign.menuAction())
        self.menubar.addAction(self.menu_ModelGen.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.action_NewProject)
        self.toolBar.addAction(self.action_OpenProject)
        self.toolBar.addAction(self.action_Export)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FracFWD"))
        self.menu_File.setTitle(_translate("MainWindow", "File"))
        self.menu_Mesh.setTitle(_translate("MainWindow", "Mesh"))
        self.menu_Background.setTitle(_translate("MainWindow", "Background"))
        self.menu_WellPath.setTitle(_translate("MainWindow", "Well Path"))
        self.menu_SurveyDesign.setTitle(_translate("MainWindow", "Survey design"))
        self.menu_ImportConfig.setTitle(_translate("MainWindow", "Import Survey Config"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menu_ModelGen.setTitle(_translate("MainWindow", "Model Generator"))
        self.menu_SlabGen.setTitle(_translate("MainWindow", "Slabs"))
        self.menu_Help.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_NewProject.setText(_translate("MainWindow", "New Project"))
        self.action_NewProject.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_OpenProject.setText(_translate("MainWindow", "Open Project"))
        self.action_OpenProject.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Export.setText(_translate("MainWindow", "Export"))
        self.action_Export.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_CropModels.setText(_translate("MainWindow", "Crop Models"))
        self.action_Exit.setText(_translate("MainWindow", "Exit"))
        self.action_Exit.setShortcut(_translate("MainWindow", "Esc"))
        self.action_NewMesh.setText(_translate("MainWindow", "New"))
        self.action_ImportMesh.setText(_translate("MainWindow", "Import"))
        self.action_ViewMesh.setText(_translate("MainWindow", "View"))
        self.action_SaveMesh.setText(_translate("MainWindow", "Save As"))
        self.action_NewBkg.setText(_translate("MainWindow", "New"))
        self.action_AddSlab.setText(_translate("MainWindow", "Add Slab"))
        self.action_AddEllipsoid.setText(_translate("MainWindow", "Add Ellipsoid"))
        self.action_ViewBkg.setText(_translate("MainWindow", "View"))
        self.action_NewSurvey.setText(_translate("MainWindow", "New"))
        self.action_ImportSrc.setText(_translate("MainWindow", "Source config"))
        self.action_ImportRcv.setText(_translate("MainWindow", "Receiver config"))
        self.action_EllipsoidGen.setText(_translate("MainWindow", "Ellipsoids"))
        self.action_About.setText(_translate("MainWindow", "About"))
        self.action_Guide.setText(_translate("MainWindow", "Guide"))
        self.action_Guide.setShortcut(_translate("MainWindow", "F1"))
        self.action_DesignWellPath.setText(_translate("MainWindow", "Design"))
        self.action_ImportWellPath.setText(_translate("MainWindow", "Import"))
        self.action_ViewSurvey.setText(_translate("MainWindow", "Survey"))
        self.action_View_added_well_paths.setText(_translate("MainWindow", "Add well paths"))
        self.action_ViewModels.setText(_translate("MainWindow", "View Models"))
        self.action_RectangularSlab.setText(_translate("MainWindow", "Rectangular plate"))
        self.action_OctagonalSlab.setText(_translate("MainWindow", "Octagonal plate"))
        self.action_DiskSlab.setText(_translate("MainWindow", "Disk"))
