from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QMessageBox
from PyQt5.QtWidgets import QLabel, QFileSystemModel
from PyQt5 import QtCore

from UI_init.Ui_MainWin import Ui_MainWindow
from UI_init.Ui_NewProj import Ui_Dialog

from GUI.Export import ExportDialog
from GUI.CropModels import CropModelDialog
from GUI.TabMesh import AddTabMesh
from GUI.TabBkg import AddTabBkg
from GUI.TabSurvey import AddTabSurvey
from GUI.AddModel import AddSlabDialog, AddEllipsoidDialog
from GUI.AddModel import AddRandomSlabDialog, AddRandomEllipsoidDialog
from GUI.pyvistaWin import pyvistaWin
from GUI.SelectWin import SelectWin
from GUI.DoubleSelectWin import DoubleSelectWin

from functions.utils import read_mesh_file

import numpy as np
import os
import shutil


def track_error(func):
    def wrapper(self):
        try:
            func(self)
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def track_error_args(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def finished_reminder(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Finished', 'Task finished.', QMessageBox.Yes)
    return wrapper


def not_finished_yet(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Information', 'NOT FINISHED YET...', QMessageBox.Yes)
    return wrapper


class NewProjDialog(Ui_Dialog, QDialog):
    def __init__(self):
        super(NewProjDialog, self).__init__()
        self.setupUi(self)
        self.create_flag = False
        self.pushButton_browser.clicked.connect(self.new_project_browser)
        self.pushButton_create.clicked.connect(self.create_new_project)

    @track_error
    def new_project_browser(self):
        project_folder = QFileDialog.getExistingDirectory(self,
                                                          "Select a project folder",
                                                          "./")
        if project_folder:
            self.LineEdit_ProjDir.setText(project_folder)

    @track_error
    def create_new_project(self):
        if self.LineEdit_ProjName.text() and self.LineEdit_ProjDir.text():
            self.create_flag = True
            self.close()
        else:
            QMessageBox.warning(self, 'Warning',
                                'Please declare both project folder and filename!',
                                QMessageBox.Yes)

    def closeEvent(self, event):
        if not self.create_flag:
            reply = QMessageBox.question(self, 'Information',
                                         'Do you want to quit\nwithout creating a new project?',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


class FracMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(FracMainWindow, self).__init__()
        self.setupUi(self)
        self.set_statusbar()
        self.New_Dir = [['Mesh'],
                        ['Background'],
                        ['Model'],
                        ['Survey'],
                        ['Survey', 'Source'],
                        ['Survey', 'Receiver'],
                        ['Wellpath']
                        ]

        self.win_list = []

        self.initial_interface()

        self.tabWidget.tabCloseRequested.connect(self.tab_close)
        self.tabWidget.currentChanged.connect(self.check_current_tab)

        # File menu
        self.action_NewProject.triggered.connect(self.new_project)
        self.action_OpenProject.triggered.connect(self.open_project)
        self.action_Export.triggered.connect(self.export)
        self.action_CropModels.triggered.connect(self.crop_model)
        self.action_ViewModels.triggered.connect(self.view_win)

        # Mesh menu
        self.action_NewMesh.triggered.connect(self.new_mesh)
        self.action_ImportMesh.triggered.connect(self.import_mesh)
        self.action_ViewMesh.triggered.connect(self.view_mesh)
        self.action_SaveMesh.triggered.connect(self.save_mesh)

        # Background menu
        self.action_NewBkg.triggered.connect(self.new_bkg)
        self.action_ImportWellPath.triggered.connect(self.import_wellpath)
        self.action_AddSlab.triggered.connect(self.add_slab)
        self.action_AddEllipsoid.triggered.connect(self.add_ellipsoid)
        self.action_ViewBkg.triggered.connect(self.view_bkg)

        # Survey Design menu
        self.action_NewSurvey.triggered.connect(self.new_survey)
        self.action_ImportSrc.triggered.connect(self.import_src)
        self.action_ImportRcv.triggered.connect(self.import_rcv)
        self.action_ViewSurvey.triggered.connect(self.view_survey)
        self.action_View_added_well_paths.triggered.connect(self.view_added_wellpaths)

        # Model generation menu
        self.action_OctagonalSlab.triggered.connect(self.slab_random_generation)
        self.action_EllipsoidGen.triggered.connect(self.ellipsoid_random_generation)

    def set_statusbar(self):
        label = QLabel('中国石油集团东方地球物理勘探有限责任公司')
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.statusBar().addWidget(label, 1)

    # --- File menu ---
    @track_error
    def new_project(self):
        new_proj_win = NewProjDialog()
        new_proj_win.exec_()

        # ./ relative path??
        # self.project_dir = os.path.join(new_proj_win.LineEdit_ProjDir.text(),
        #                                 new_proj_win.LineEdit_ProjName.text())
        # if self.project_dir:

        if new_proj_win.create_flag:
            self.project_dir = os.path.join(new_proj_win.LineEdit_ProjDir.text(),
                                            new_proj_win.LineEdit_ProjName.text())
            for dir in self.New_Dir:
                if not os.path.exists(os.path.join(self.project_dir, *dir)):
                    os.makedirs(os.path.join(os.path.join(self.project_dir, *dir)))

            self.after_open_proj()

    @track_error
    def open_project(self):
        # add checking project structure
        project_dir = QFileDialog.getExistingDirectory(self,
                                                       "Select a project folder",
                                                       "./")

        if project_dir:
            self.project_dir = project_dir
            self.after_open_proj()

    @track_error
    def export(self):
        export_win = ExportDialog(self.project_dir)
        export_win.exec()

    @track_error
    def crop_model(self):
        crop_win = CropModelDialog()
        crop_win.exec()

    @track_error
    def view_win(self):
        self.win_list.append(pyvistaWin())
        # self.mesh_view_win = pyvistaWin()
        self.win_list[-1].show()

    # --- Mesh menu ---
    @track_error
    def new_mesh(self):
        tab_mesh = AddTabMesh(self.project_dir)
        self.tabWidget.addTab(tab_mesh, 'Mesh')
        self.tabWidget.setCurrentWidget(tab_mesh)
        # what if I close this tab?

    @track_error
    @finished_reminder
    def import_mesh(self):
        imported_mesh_path = QFileDialog.getOpenFileName(self, 'Import mesh file', '.\\', '*.txt')
        # copy external mesh file to current project folder
        shutil.copy(imported_mesh_path[0], os.path.join(self.project_dir, 'Mesh'))

    @track_error
    def view_mesh(self):
        mesh_select_win = SelectWin(os.path.join(self.project_dir, 'Mesh'), 'mesh')
        mesh_select_win.exec()
        if mesh_select_win.select_flag:
            nodeX, nodeY, nodeZ = read_mesh_file(mesh_select_win.selected_path)

            self.mesh_view_win = pyvistaWin()
            self.mesh_view_win.label_MeshPath.setText(mesh_select_win.selected_path)
            self.mesh_view_win.view_model_ubc(nodeY, nodeX, nodeZ, None)
            self.mesh_view_win.show()

    @track_error
    def save_mesh(self):
        mesh_path = QFileDialog.getSaveFileName(self, 'Save Your Mesh', '.\\', '*.txt')
        if mesh_path[0]:
            try:
                self.tab_mesh.write_mesh_file(mesh_path=mesh_path[0])
            except AttributeError:
                QMessageBox.warning(self, 'Warning', 'Please mesh design at first!',
                                    QMessageBox.Yes)

    # --- Background menu ---
    @track_error
    def new_bkg(self):
        tab_bkg = AddTabBkg(self.project_dir)
        self.tabWidget.addTab(tab_bkg, 'Background')
        self.tabWidget.setCurrentWidget(tab_bkg)
        # what if I close this tab?

    @track_error
    def import_wellpath(self):
        tab_bkg = self.tabWidget.currentWidget()
        tab_bkg.groupBox_edgeCon.setEnabled(True)
        tab_bkg.import_wellpath()

    @track_error
    def add_slab(self):
        slab_win = AddSlabDialog(self.project_dir)
        slab_win.setWindowTitle('Add Slab')
        slab_win.show()
        slab_win.exec()

    @track_error
    def add_ellipsoid(self):
        ellipsoid_win = AddEllipsoidDialog(self.project_dir)
        ellipsoid_win.setWindowTitle('Add Ellipsoid')
        ellipsoid_win.show()
        ellipsoid_win.exec()

    @track_error
    def view_bkg(self):
        # open selector dialog
        mesh_model_select_win = DoubleSelectWin([os.path.join(self.project_dir, 'Mesh'),
                                                 os.path.join(self.project_dir, 'Background')],
                                                ['mesh', 'background'])
        mesh_model_select_win.exec()
        if mesh_model_select_win.select_flag:
            nodeX, nodeY, nodeZ = read_mesh_file(mesh_model_select_win.selected_path_left)
            model_in = np.loadtxt(mesh_model_select_win.selected_path_right)
            self.view_win = pyvistaWin()
            self.view_win.label_MeshPath.setText(mesh_model_select_win.selected_path_left)
            self.view_win.label_ModelPath.setText(mesh_model_select_win.selected_path_right)
            self.view_win.view_model_ubc(nodeY, nodeX, nodeZ, model_in)
            self.view_win.show()

    # --- Survey design menu ---
    @track_error
    def new_survey(self):
        tab_survey = AddTabSurvey(self.project_dir)
        self.tabWidget.addTab(tab_survey, 'Survey Design')
        self.tabWidget.setCurrentWidget(tab_survey)
        # what if I close this tab?

    @track_error
    def import_src(self):
        tab_survey = self.tabWidget.currentWidget()
        tab_survey.import_src()

    @track_error
    def import_rcv(self):
        receiver_dir, tmp = QFileDialog.getOpenFileName(self,
                                                        "Choose receiver file",
                                                        "*")
        if receiver_dir:
            # copy file
            shutil.copy(receiver_dir, os.path.join(self.project_dir, *['Survey', 'Receiver']))

            tab_survey = self.tabWidget.currentWidget()
            tab_survey.label_rcvfile.setText('receiver config filename: ' + receiver_dir.split('/')[-1])
            tab_survey.import_rcv()
            tab_survey.deactivate_rcv_setting()

    @track_error
    def view_survey(self):
        if self.tabWidget.currentWidget():
            if self.tabWidget.currentWidget().objectName() == 'tab_survey':
                tab_survey = self.tabWidget.currentWidget()
                tab_survey.view_survey()
            else:
                self.new_survey()
                tab_survey = self.tabWidget.currentWidget()
                tab_survey.view_survey()
        else:
            self.new_survey()
            tab_survey = self.tabWidget.currentWidget()
            tab_survey.view_survey()

    def view_added_wellpaths(self):
        if self.tabWidget.currentWidget():
            if self.tabWidget.currentWidget().objectName() == 'tab_survey':
                tab_survey = self.tabWidget.currentWidget()
                tab_survey.view_added_wellpaths()
            else:
                self.new_survey()
                tab_survey = self.tabWidget.currentWidget()
                tab_survey.view_added_wellpaths()
        else:
            self.new_survey()
            tab_survey = self.tabWidget.currentWidget()
            tab_survey.view_added_wellpaths()

    # --- Model generation menu ---
    @track_error
    def slab_random_generation(self):
        slab_random_win = AddRandomSlabDialog(self.project_dir)
        slab_random_win.setWindowTitle('Random Slab (Octagonal plate)')
        slab_random_win.show()
        slab_random_win.exec()

    @track_error
    def ellipsoid_random_generation(self):
        slab_random_win = AddRandomEllipsoidDialog(self.project_dir)
        slab_random_win.setWindowTitle('Random Ellipsoid')
        slab_random_win.show()
        slab_random_win.exec()

    # other GUI functions
    def tab_close(self, index):
        self.tabWidget.removeTab(index)

    def check_current_tab(self):
        self.action_SaveMesh.setEnabled(False)
        self.action_ImportWellPath.setEnabled(False)
        self.action_ImportSrc.setEnabled(False)
        self.action_ImportRcv.setEnabled(False)
        if self.tabWidget.currentWidget() is not None:
            if self.tabWidget.currentWidget().objectName() == 'tab_mesh':
                self.action_SaveMesh.setEnabled(True)
            elif self.tabWidget.currentWidget().objectName() == 'tab_bkg':
                self.action_ImportWellPath.setEnabled(True)
            elif self.tabWidget.currentWidget().objectName() == 'tab_survey':
                self.action_ImportSrc.setEnabled(True)
                self.action_ImportRcv.setEnabled(True)

    @track_error
    def initial_interface(self):
        # File menu
        self.action_Export.setEnabled(False)

        # Mesh menu
        self.menu_Mesh.setEnabled(False)
        self.action_SaveMesh.setEnabled(False)

        # Background menu
        self.menu_Background.setEnabled(False)
        self.action_ImportWellPath.setEnabled(False)

        # Survey Design menu
        self.menu_SurveyDesign.setEnabled(False)
        self.action_ImportSrc.setEnabled(False)
        self.action_ImportRcv.setEnabled(False)
        # self.action_View_added_well_paths.setEnabled(False)

        # Model generation menu
        self.menu_ModelGen.setEnabled(False)

        # main win
        self.tabWidget.setVisible(False)
        self.treeView.setVisible(False)

    @track_error
    def after_open_proj(self):
        self.file_browser(self.project_dir)
        self.tabWidget.setVisible(True)
        self.treeView.setVisible(True)

        self.action_Export.setEnabled(True)
        self.menu_Mesh.setEnabled(True)
        self.menu_Background.setEnabled(True)
        self.menu_SurveyDesign.setEnabled(True)
        self.menu_ModelGen.setEnabled(True)

    @track_error_args
    def file_browser(self, project_dir):
        model = QFileSystemModel()
        model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(project_dir))

        self.treeView.expandAll()
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)
        self.treeView.setSortingEnabled(True)
