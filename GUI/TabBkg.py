from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from UI_init.Ui_tabBkg import Ui_tab_bkg as Ui_TabBkg

from GUI.SelectWin import SelectWin
from GUI.pyvistaWin import pyvistaWin
from GUI.FilenameSetting import FileNameSettingWin
from GUI.XYZTable import XYZTable

from functions.utils import read_mesh_file, formRectMeshConnectivity
from functions.addSurface import addSurface
from functions.wellpath2edge import wellpath2edge

import os
import numpy as np
from scipy.spatial import ConvexHull


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
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def finished_reminder(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Finished', 'Task finished.', QMessageBox.Yes)
    return wrapper


class AddTabBkg(QTabWidget, Ui_TabBkg):
    def __init__(self, path):
        super(AddTabBkg, self).__init__()
        self.setupUi(self)
        self.project_dir = path

        self.renew_tab_well_table(0, 'Wellpath points')

        self.nodeX = None
        self.nodeY = None
        self.nodeZ = None

        self.build_model_init()

        self.groupBox_CellCon.setEnabled(False)
        self.groupBox_edgeCon.setEnabled(False)

        self.pushButton_meshBrowser.clicked.connect(self.load_mesh)

        # cellCon
        self.lineEdit_numLayers.editingFinished.connect(self.layer_table_init)
        self.pushButton_build.clicked.connect(self.build_model)
        self.pushButton_viewModel.clicked.connect(self.view_model)
        self.pushButton_save_cellCon.clicked.connect(self.save_model)
        # edgeCon
        self.checkBox_int.setChecked(False)
        self.checkBox_edgeCon.setChecked(False)
        self.edgeCon_int_setting()
        self.checkBox_int.stateChanged.connect(self.edgeCon_int_setting)
        self.checkBox_edgeCon.stateChanged.connect(self.edgeCon_int_setting)
        self.tabWidget_wellpath.currentChanged.connect(self.show_points_num)
        self.lineEdit_edgeCon.editingFinished.connect(self.uniform_edgeCon)
        self.lineEdit_Npoints.editingFinished.connect(self.tab_well_table_update)
        self.pushButton_clear.clicked.connect(self.redesign_edgeCon)
        self.pushButton_save_edgeCon.clicked.connect(self.build_edgeCon)
        self.pushButton_importwellpath.clicked.connect(self.import_wellpath)
        # self.groupBox_edgeCon.toggled.connect(self.build_edgeCon)

    @track_error
    def load_mesh(self):
        mesh_select_win = SelectWin(os.path.join(self.project_dir, 'Mesh'), 'mesh')
        mesh_select_win.exec()
        if mesh_select_win.select_flag:
            self.nodeX, self.nodeY, self.nodeZ = read_mesh_file(mesh_select_win.selected_path)
            self.lineEdit_meshpath.setText(mesh_select_win.selected_path)
            self.groupBox_edgeCon.setEnabled(True)
            self.groupBox_CellCon.setEnabled(True)

    @track_error
    def layer_table_init(self):
        self.layers_num = int(self.lineEdit_numLayers.text())
        self.tableWidget_layered.setRowCount(self.layers_num)
        self.Push = [0] * (self.layers_num - 1)
        for i in range(self.layers_num):
            item = QTableWidgetItem()
            self.tableWidget_layered.setVerticalHeaderItem(i, item)
            self.tableWidget_layered.verticalHeader().setDefaultSectionSize(30)
            self.tableWidget_layered.verticalHeader().setMinimumSectionSize(20)
            self.tableWidget_layered.verticalHeaderItem(i).setText(("Layer" + str(i + 1)))
            self.tableWidget_layered.setItem(i, 0, item)

            if i < self.layers_num - 1:
                self.Push[i] = QPushButton()
                self.Push[i].setText('Load')
                self.Push[i].setObjectName(str(i))
                # combox.setStyleSheet("QPushButton{background:white}")
                self.tableWidget_layered.setCellWidget(i, 1, self.Push[i])

        for i in range(len(self.Push)):
            self.Push[i].clicked.connect(self.find_surface_config)

    @track_error
    def find_surface_config(self):
        ind = int(self.sender().objectName())
        fileName = QFileDialog.getOpenFileName(self.Push[ind], 'Load Surface', '.\\', '*.txt')
        if fileName[0]:
            item = QTableWidgetItem()
            self.tableWidget_layered.setItem(ind, 2, item)
            self.tableWidget_layered.item(ind, 2).setText(fileName[0])

    @track_error_args
    def load_surface_config(self, surface_config_path):
        sfLocInfo = np.loadtxt(surface_config_path, delimiter=',')
        # with open(surface_config_path, 'r') as f:
        #     ff = f.readlines()
        #     size = len(ff)
        #     sfLocInfo = np.zeros((size, 3))
        #     for i in range(size):
        #         sp = ff[i].split(',')
        #         sfLocInfo[i, 0] = float(sp[0])
        #         sfLocInfo[i, 1] = float(sp[1])
        #         sfLocInfo[i, 2] = float(sp[2])
        return sfLocInfo

    def build_model_init(self):
        self.model_out = None
        self.pushButton_viewModel.setEnabled(False)
        self.pushButton_save_cellCon.setEnabled(False)

    @track_error
    def build_model(self):
        self.build_model_init()
        if self.layers_num == 1:
            cell = (len(self.nodeX) - 1) * (len(self.nodeY) - 1) * (len(self.nodeZ) - 1)
            if self.tableWidget_layered.item(0, 0).text():
                self.model_out = float(self.tableWidget_layered.item(0, 0).text()) * np.ones((cell, 1))
                QMessageBox.information(self,
                                        "Information",
                                        "Homogeneous model created.",
                                        QMessageBox.Yes)
                self.pushButton_viewModel.setEnabled(True)
                self.pushButton_save_cellCon.setEnabled(True)
            else:
                QMessageBox.warning(self,
                                    "Error",
                                    "Please set layer parameter!",
                                    QMessageBox.Yes)
        elif self.layers_num > 1:
            for n in range(self.layers_num - 1):
                if self.tableWidget_layered.item(n, 2) and self.tableWidget_layered.item(1, 0):
                    surface_config_path = self.tableWidget_layered.item(n, 2).text()
                    val_out = float(self.tableWidget_layered.item(n + 1, 0).text())
                    if n == 0:
                        cell = (len(self.nodeX) - 1) * (len(self.nodeY) - 1) * (len(self.nodeZ) - 1)
                        model_in = float(self.tableWidget_layered.item(0, 0).text()) * np.ones((cell, 1))
                        sfLocInfo = self.load_surface_config(surface_config_path=surface_config_path)
                        hull = ConvexHull(sfLocInfo[:, :2])
                        out_bound = np.array([[self.nodeX[0], self.nodeY[0]],
                                              [self.nodeX[-1], self.nodeY[0]],
                                              [self.nodeX[-1], self.nodeY[-1]],
                                              [self.nodeX[0], self.nodeY[-1]]])
                        new_points = np.append(sfLocInfo[:, :2], out_bound, axis=0)
                        new_hull = ConvexHull(new_points)
                        if list(hull.vertices) != list(new_hull.vertices):

                            QMessageBox.warning(self.pushButton_build,
                                                'Load Surface',
                                                '(In layer #%d) Please use a topo data whose XOY \
                                                \nis larger than that in the mesh loaded!' % (n + 1),
                                                QMessageBox.Yes)
                            break
                        self.model_out = addSurface(self.nodeX, self.nodeY, self.nodeZ, model_in,
                                                    sfLocInfo, val_out, 'z')
                    else:
                        sfLocInfo = self.load_surface_config(surface_config_path=surface_config_path)
                        hull = ConvexHull(sfLocInfo[:, :2])
                        out_bound = np.array([[self.nodeX[0], self.nodeY[0]],
                                              [self.nodeX[-1], self.nodeY[0]],
                                              [self.nodeX[-1], self.nodeY[-1]],
                                              [self.nodeX[0], self.nodeY[-1]]])
                        new_points = np.append(sfLocInfo[:, :2], out_bound, axis=0)
                        new_hull = ConvexHull(new_points)
                        if list(hull.vertices) != list(new_hull.vertices):
                            QMessageBox.warning(self.pushButton_build,
                                                'Load Surface',
                                                '(In layer #%d) Please use a topo data whose XOY \
                                                \nis larger than that in the mesh loaded!' % n,
                                                QMessageBox.Yes)
                            break
                        model_in = self.model_out
                        self.model_out = addSurface(self.nodeX, self.nodeY, self.nodeZ, model_in,
                                                    sfLocInfo, val_out, 'z')
                else:
                    QMessageBox.warning(self,
                                        "Error",
                                        "Please load #%d layer config file or set value!" % n,
                                        QMessageBox.Yes)
                    break

            if (self.nodeX is not None) and (self.model_out is not None):
                self.pushButton_viewModel.setEnabled(True)
                self.pushButton_save_cellCon.setEnabled(True)
                QMessageBox.information(self, 'Building model', 'Layered model is generated.', QMessageBox.Yes)

    @track_error
    def view_model(self):
        self.model_view_win = pyvistaWin(self.nodeX, self.nodeY, self.nodeZ, self.model_out)
        self.model_view_win.show()

    @track_error
    def save_model(self):
        save_win = FileNameSettingWin()
        project_name = self.project_dir.split('/')[-1]
        save_win.label_path.setText('%s/Background/' % project_name)
        save_win.label_filename.setText('Background filename: ')
        save_win.exec()

        if save_win.create_flag:
            model_filename = save_win.lineEdit_filename.text() + '.txt'
            model_path = os.path.join(self.project_dir, *['Background', model_filename])
            with open(model_path, 'w') as f:
                for i in range(len(self.model_out)):
                    f.write(str(float(self.model_out[i])) + "\n")
                QMessageBox.information(self, 'Saving Layered Model',
                                        'Current layered model saved.',
                                        QMessageBox.Yes)

    @track_error
    def build_edgeCon(self):
        # discrete points
        if self.checkBox_int.isChecked():
            if self.nodeX is not None:
                lengths = formRectMeshConnectivity(self.nodeX, self.nodeY, self.nodeZ)
                self.edgeCon = lengths * 0
                for k in range(self.tabWidget_wellpath.count()):
                    current_tab_table = self.tabWidget_wellpath.widget(k)
                    wellpath_ctrl_points = np.empty(shape=(current_tab_table.tableWidget.rowCount(), 3))
                    edgeCon_input_ctrl = np.empty(shape=current_tab_table.tableWidget.rowCount())
                    for i in range(current_tab_table.tableWidget.rowCount()):
                        wellpath_ctrl_points[i][0] = float(current_tab_table.tableWidget.item(i, 0).text())
                        wellpath_ctrl_points[i][1] = float(current_tab_table.tableWidget.item(i, 1).text())
                        wellpath_ctrl_points[i][2] = float(current_tab_table.tableWidget.item(i, 2).text())
                        edgeCon_input_ctrl[i] = float(current_tab_table.tableWidget.item(i, 3).text())
                    edgeCon_input_ctrl[-1] = np.nan

                    d = float(self.lineEdit_int.text())
                    assert d > 0
                    wellpath_discrete = []
                    edgeCon_input_discrete = []
                    for i in range(wellpath_ctrl_points.shape[0] - 1):
                        dx = (wellpath_ctrl_points[i + 1][0] - wellpath_ctrl_points[i][0])
                        dy = (wellpath_ctrl_points[i + 1][1] - wellpath_ctrl_points[i][1])
                        dz = (wellpath_ctrl_points[i + 1][2] - wellpath_ctrl_points[i][2])
                        length = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
                        n = np.ceil(length / d)
                        for j in range(int(n)):
                            wellpath_discrete.append([wellpath_ctrl_points[i][0] + j * d * (dx / length),
                                                      wellpath_ctrl_points[i][1] + j * d * (dy / length),
                                                      wellpath_ctrl_points[i][2] + j * d * (dz / length)])
                            edgeCon_input_discrete.append(edgeCon_input_ctrl[i])
                        wellpath_discrete.append([wellpath_ctrl_points[i + 1][0] - (length % d) * (dx / length),
                                                  wellpath_ctrl_points[i + 1][1] - (length % d) * (dy / length),
                                                  wellpath_ctrl_points[i + 1][2] - (length % d) * (dz / length)])
                        edgeCon_input_discrete.append(edgeCon_input_ctrl[i + 1])

                    edgeCon_tmp = wellpath2edge(nodeX=self.nodeX, nodeY=self.nodeY, nodeZ=self.nodeZ,
                                                wellpath=np.array(wellpath_discrete),
                                                wellCon=np.array(edgeCon_input_discrete[:-1]))
                    # edgeCon_tmp = wellpath2edge(nodeX=self.nodeX, nodeY=self.nodeY, nodeZ=self.nodeZ,
                    #                             wellpath=np.array(wellpath_discrete),
                    #                             wellCon=np.array(edgeCon_input_discrete))

                    # print(np.where(edgeCon_tmp != 0))
                    # for i in np.where(edgeCon_tmp != 0):
                    #     print('edgeCon are: ', edgeCon_tmp[i])
                    self.edgeCon = self.edgeCon + edgeCon_tmp
                self.save_edgeCon()
            else:
                QMessageBox.warning(self, 'Error',
                                    'Please set mesh file!',
                                    QMessageBox.Yes)
        # ctrl points
        else:
            if self.nodeX is not None:
                # zeros
                lengths = formRectMeshConnectivity(self.nodeX, self.nodeY, self.nodeZ)
                self.edgeCon = lengths * 0
                for k in range(self.tabWidget_wellpath.count()):
                    current_tab_table = self.tabWidget_wellpath.widget(k)
                    wellpath_ctrl_points = np.empty(shape=(current_tab_table.tableWidget.rowCount(), 3))
                    edgeCon_input_ctrl = np.empty(shape=current_tab_table.tableWidget.rowCount())
                    for i in range(current_tab_table.tableWidget.rowCount()):
                        wellpath_ctrl_points[i][0] = float(current_tab_table.tableWidget.item(i, 0).text())
                        wellpath_ctrl_points[i][1] = float(current_tab_table.tableWidget.item(i, 1).text())
                        wellpath_ctrl_points[i][2] = float(current_tab_table.tableWidget.item(i, 2).text())
                        edgeCon_input_ctrl[i] = float(current_tab_table.tableWidget.item(i, 3).text())
                    edgeCon_input_ctrl[-1] = np.nan

                    edgeCon_tmp = wellpath2edge(nodeX=self.nodeX, nodeY=self.nodeY, nodeZ=self.nodeZ,
                                                wellpath=np.array(wellpath_ctrl_points),
                                                wellCon=edgeCon_input_ctrl[:-1])
                    # edgeCon_tmp = wellpath2edge(nodeX=self.nodeX, nodeY=self.nodeY, nodeZ=self.nodeZ,
                    #                             wellpath=np.array(wellpath_ctrl_points),
                    #                             wellCon=edgeCon_input_ctrl)

                    # print(np.where(edgeCon_tmp != 0))
                    # for i in np.where(edgeCon_tmp != 0):
                    #     print('edgeCon are: ', edgeCon_tmp[i])
                    self.edgeCon = self.edgeCon + edgeCon_tmp
                self.save_edgeCon()
            else:
                QMessageBox.warning(self, 'Error',
                                    'Please set mesh file!',
                                    QMessageBox.Yes)

    @track_error
    def uniform_edgeCon(self):
        # returnPressed?
        reply = QMessageBox.information(self,
                                        'Information',
                                        'Do you want to set all edgeCon value at %.f?' % float(self.lineEdit_edgeCon.text()),
                                        QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i in range(self.tabWidget_wellpath.count()):
                current_tab_table = self.tabWidget_wellpath.widget(i)
                edgeCon_ctrl_points = np.ones((current_tab_table.tableWidget.rowCount())) * float(self.lineEdit_edgeCon.text())
                current_tab_table.points_to_table_column(edgeCon_ctrl_points, 3)

    @track_error
    def save_edgeCon(self):
        save_win = FileNameSettingWin()
        project_name = self.project_dir.split('/')[-1]
        save_win.label_path.setText('%s/Wellpath/' % project_name)
        save_win.label_filename.setText('Wellpath filename: ')
        save_win.exec()

        if save_win.create_flag:
            wellpath_filename = 'edgeCon_' +save_win.lineEdit_filename.text() + '.txt'
            wellpath_path = os.path.join(self.project_dir, *['Wellpath', wellpath_filename])
            np.savetxt(wellpath_path, self.edgeCon)
            QMessageBox.information(self, 'Saving edgeCon',
                                    'edgeCon data for wellpath saved.',
                                    QMessageBox.Yes)

    # @track_error
    def import_wellpath(self):
        wellpath_paths = QFileDialog.getOpenFileNames(self,
                                                      "Choose wellpath points files",
                                                      "*.txt")
        if wellpath_paths[0]:
            self.tabWidget_wellpath.clear()
            self.lineEdit_int.clear()
            self.lineEdit_Npoints.clear()
            self.lineEdit_int.setEnabled(False)
            self.lineEdit_Npoints.setEnabled(False)
            self.checkBox_edgeCon.setChecked(False)
            for i in range(len(wellpath_paths[0])):
                wellpath_path = wellpath_paths[0][i]
                well_points = np.loadtxt(wellpath_path, delimiter=',')
                self.add_tab_well_table(well_points.shape[0], os.path.split(wellpath_path)[1])
                # self.add_tab_well_table(well_points.shape[0], os.path.split(os.path.splitext(wellpath_path)[0])[1])
                tab_wellpath_points = self.tabWidget_wellpath.currentWidget()
                tab_wellpath_points.points_to_table(well_points)
            self.lineEdit_Npoints.setText(str(tab_wellpath_points.tableWidget.rowCount()))

    def redesign_edgeCon(self):
        self.lineEdit_edgeCon.setEnabled(True)
        self.lineEdit_edgeCon.clear()
        self.lineEdit_Npoints.setEnabled(True)
        self.lineEdit_Npoints.clear()
        self.lineEdit_int.setEnabled(True)
        self.lineEdit_int.clear()
        self.renew_tab_well_table(0, 'Wellpath points')

    @track_error
    def edgeCon_int_setting(self):
        if self.checkBox_int.isChecked():
            self.lineEdit_int.setEnabled(True)
        else:
            self.lineEdit_int.setEnabled(False)

        if self.checkBox_edgeCon.isChecked():
            self.lineEdit_edgeCon.setEnabled(True)
        else:
            self.lineEdit_edgeCon.setEnabled(False)
            self.clear_edgeCon_cloumn()

    def clear_edgeCon_cloumn(self):
        if self.lineEdit_edgeCon.text():
            self.lineEdit_edgeCon.clear()
            tab_wellpath_points = self.tabWidget_wellpath.currentWidget()
            if tab_wellpath_points:
                tab_wellpath_points.clear_table_column(3)
                QMessageBox.warning(self, 'Clear edgeCon Value',
                                    'edgeCon values will be cleared?',
                                    QMessageBox.Yes)

    @track_error
    def show_points_num(self):
        tab_wellpath_points = self.tabWidget_wellpath.currentWidget()
        if tab_wellpath_points:
            self.lineEdit_Npoints.setText(str(tab_wellpath_points.tableWidget.rowCount()))

    # @track_error_args
    def renew_tab_well_table(self, row, tab_name):
        self.tabWidget_wellpath.clear()
        tab_wellpath_data = XYZTable(nc=4, Hheaders=['X', 'Y', 'Z', 'edgeCon'])
        tab_wellpath_data.table_init(row)
        self.tabWidget_wellpath.addTab(tab_wellpath_data, tab_name)
        self.tabWidget_wellpath.setCurrentWidget(tab_wellpath_data)

    # @track_error_args
    def add_tab_well_table(self, row, tab_name):
        tab_wellpath_data = XYZTable(nc=4, Hheaders=['X', 'Y', 'Z', 'edgeCon'])
        tab_wellpath_data.table_init(row)
        self.tabWidget_wellpath.addTab(tab_wellpath_data, tab_name)
        self.tabWidget_wellpath.setCurrentWidget(tab_wellpath_data)

    # @track_error
    def tab_well_table_update(self):
        self.tabWidget_wellpath.clear()
        self.renew_tab_well_table(int(self.lineEdit_Npoints.text()), 'Wellpath points')
        if self.lineEdit_edgeCon.text():
            tab_wellpath_points = self.tabWidget_wellpath.currentWidget()
            edgeCon_ctrl_points = np.ones((tab_wellpath_points.tableWidget.rowCount())) * float(
                self.lineEdit_edgeCon.text())
            tab_wellpath_points.points_to_table_column(edgeCon_ctrl_points, 3)
