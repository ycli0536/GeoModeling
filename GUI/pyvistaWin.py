from PyQt5.QtCore import pyqtSignal, Qt, QSettings
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
from UI_init.Ui_ViewWin import Ui_MainWindow
from UI_init.Ui_CropModels import Ui_Dialog as Ui_CropDialog
from UI_init.Ui_thresholdWin import Ui_Dialog as Ui_ThresholdDialog
from functions.utils import read_mesh_file, CellIndex2PointXYZ
from functions.decorators import track_error, track_error_args
from functions.config_setting import get_setting_values, set_setting_values
from pyvistaqt import QtInteractor, MainWindow

import numpy as np
import pyvista as pv


class CropModelDialog(QDialog, Ui_CropDialog):
    signal = pyqtSignal(np.ndarray, np.ndarray, np.ndarray, np.ndarray)

    def __init__(self, nodeX, nodeY, nodeZ, model_in):
        super(CropModelDialog, self).__init__()
        self.setupUi(self)
        self.get_config()

        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ
        self.model_in = model_in

        self.commandLinkBtn_datapath.setEnabled(False)
        self.commandLinkBtn_outputpath.setEnabled(False)
        self.label_datapath.setEnabled(False)
        self.label_outputpath.setEnabled(False)
        self.pushButton_crop.clicked.connect(self.crop)

    @track_error
    def get_config(self):
        self.config_type = 'CROP'
        self.config_name = ['x_min', 'x_max',
                            'y_min', 'y_max',
                            'z_min', 'z_max',
                            'window_width', 'window_height',
                            'window_pos_x', 'window_pos_y']
        init_variables = get_setting_values(self.config_type, self.config_name)
        self.lineEdit_Xmin.setText(init_variables[0])
        self.lineEdit_Xmax.setText(init_variables[1])
        self.lineEdit_Ymin.setText(init_variables[2])
        self.lineEdit_Ymax.setText(init_variables[3])
        self.lineEdit_Zmin.setText(init_variables[4])
        self.lineEdit_Zmax.setText(init_variables[5])
        if init_variables[6]:
            self.resize(init_variables[6], init_variables[7])
        if init_variables[8]:
            self.move(init_variables[8], init_variables[9])

    def crop(self):
        try:
            xmin = float(self.lineEdit_Xmin.text())
            xmax = float(self.lineEdit_Xmax.text())
            assert self.nodeX[0] < xmin < xmax < self.nodeX[-1]

            ymin = float(self.lineEdit_Ymin.text())
            ymax = float(self.lineEdit_Ymax.text())
            assert self.nodeY[0] < ymin < ymax < self.nodeY[-1]

            zmin = float(self.lineEdit_Zmin.text())
            zmax = float(self.lineEdit_Zmax.text())
            assert self.nodeZ[-1] < zmin < zmax < self.nodeZ[0]

            indx = (xmin <= self.nodeX) & (xmax >= self.nodeX)
            indy = (ymin <= self.nodeY) & (ymax >= self.nodeY)
            indz = (zmin <= self.nodeZ) & (zmax >= self.nodeZ)

            sub_nodeX = self.nodeX[indx]
            sub_nodeY = self.nodeY[indy]
            sub_nodeZ = self.nodeZ[indz]

            temp = CellIndex2PointXYZ(self.nodeX, self.nodeY, self.nodeZ, [])
            x = temp[:, 0]
            y = temp[:, 1]
            z = temp[:, 2]

            # original model vector -> cropped model vector (UBC format)
            cropped_model = np.empty((len(sub_nodeY) - 1, len(sub_nodeX) - 1, len(sub_nodeZ) - 1))

            ind = (x >= sub_nodeX[0]) & (x <= sub_nodeX[-1]) & \
                  (y >= sub_nodeY[0]) & (y <= sub_nodeY[-1]) & \
                  (z <= sub_nodeZ[0]) & (z >= sub_nodeZ[-1])
            cropped_model_v = self.model_in[ind]

            self.signal.emit(sub_nodeX, sub_nodeY, sub_nodeZ, cropped_model_v)

            QMessageBox.information(self.pushButton_crop,
                                    'Model Cropping',
                                    'Model is cropped.',
                                    QMessageBox.Yes)

        except AssertionError:
            QMessageBox.warning(self.pushButton_crop,
                                "Error",
                                "Pleas set right sub-space!",
                                QMessageBox.Yes)

    def closeEvent(self, event):
        variables = [self.lineEdit_Xmin.text(), self.lineEdit_Xmax.text(),
                     self.lineEdit_Ymin.text(), self.lineEdit_Ymax.text(),
                     self.lineEdit_Zmin.text(), self.lineEdit_Zmax.text(),
                     self.rect().width(), self.rect().height(),
                     self.pos().x(), self.pos().y()]
        set_setting_values(module_name=self.config_type, variable_names=self.config_name, variables=variables)


class ThresholdDialog(QDialog, Ui_ThresholdDialog):
    signal = pyqtSignal(float, float)

    def __init__(self, model_in):
        super(ThresholdDialog, self).__init__()
        self.setupUi(self)
        self.get_config()
        self.model_in = model_in
        self.horizontalSlider_max.setMaximum(self.model_in.max())
        self.horizontalSlider_max.setMinimum(self.model_in.min())
        self.horizontalSlider_min.setMaximum(self.model_in.max())
        self.horizontalSlider_min.setMinimum(self.model_in.min())
        # self.horizontalSlider_max.setSingleStep((self.model_in.max() - self.model_in.min()) / 100)
        # self.horizontalSlider_min.setSingleStep((self.model_in.max() - self.model_in.min()) / 100)
        self.lineEdit_max.setText(str(self.model_in.max()))
        self.lineEdit_min.setText(str(self.model_in.min()))
        self.horizontalSlider_max.setValue(self.model_in.max())

        self.lineEdit_max.editingFinished.connect(self.update_slider_max)
        self.lineEdit_min.editingFinished.connect(self.update_slider_min)
        self.lineEdit_max.editingFinished.connect(self.signal_emit)
        self.lineEdit_min.editingFinished.connect(self.signal_emit)
        self.horizontalSlider_max.valueChanged.connect(self.slider_value_changed_max)
        self.horizontalSlider_min.valueChanged.connect(self.slider_value_changed_min)
        self.horizontalSlider_max.sliderReleased.connect(self.signal_emit)
        self.horizontalSlider_min.sliderReleased.connect(self.signal_emit)

    @track_error
    def get_config(self):
        self.config_type = 'THRESHOLD'
        self.config_name = ['window_width', 'window_height',
                            'window_pos_x', 'window_pos_y']
        init_variables = get_setting_values(self.config_type, self.config_name)

        if init_variables[0]:
            self.resize(init_variables[0], init_variables[1])
        if init_variables[2]:
            self.move(init_variables[2], init_variables[3])

    @track_error
    def update_slider_max(self):
        if self.lineEdit_max.text():
            max_val = float(self.lineEdit_max.text())
            self.horizontalSlider_max.setValue(max_val)

    @track_error
    def update_slider_min(self):
        if self.lineEdit_min.text():
            min_val = float(self.lineEdit_min.text())
            self.horizontalSlider_min.setValue(min_val)

    @track_error
    def slider_value_changed_max(self):
        if self.lineEdit_max.text():
            value_show = float(self.horizontalSlider_max.value())
            self.lineEdit_max.setText(str(value_show))

    @track_error
    def slider_value_changed_min(self):
        if self.lineEdit_min.text():
            value_show = float(self.horizontalSlider_min.value())
            self.lineEdit_min.setText(str(value_show))

    @track_error
    def signal_emit(self):
        self.signal.emit(float(self.lineEdit_min.text()), float(self.lineEdit_max.text()))

    @track_error
    def accepted(self):
        self.signal.emit(float(self.lineEdit_min.text()), float(self.lineEdit_max.text()))

    @track_error
    def rejected(self):
        self.signal.emit(self.model_in.min(), self.model_in.min())

    @track_error_args
    def closeEvent(self, event):
        variables = [self.rect().width(), self.rect().height(),
                     self.pos().x(), self.pos().y()]
        set_setting_values(module_name=self.config_type, variable_names=self.config_name, variables=variables)


class pyvistaWin(MainWindow, Ui_MainWindow):
    def __init__(self):
        super(pyvistaWin, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.model_flag = True
        self.bounding_box_flag = False
        self.bounds_flag = True
        self.log_flag = False
        self.ticks = 'real'
        self.orientation_marker_flag = False
        self.reverse_xy_flag = False

        self.add_mode = False
        self.action_Threshold.setEnabled(False)

        self.nodeX = None
        self.nodeY = None
        self.nodeZ = None
        self.model_in = None

        self.plotter = QtInteractor()
        self.verticalLayout.addWidget(self.plotter.interactor)

        self.get_config()

        # menu File
        self.action_Load.triggered.connect(self.load_mesh_model)
        self.action_Add.triggered.connect(self.add_mesh_model)
        self.commandLinkButton_mesh.clicked.connect(self.load_mesh)
        self.commandLinkButton_model.clicked.connect(self.load_model)

        # menu View
        self.action_PyVista.triggered.connect(self.display_model_pyvista)
        self.action_UBC.triggered.connect(self.display_model_ubc)

        self.action_Wireframe.triggered.connect(self.wireframe)
        self.action_BoundingBox.triggered.connect(self.bounding_box)
        self.action_Bounds.triggered.connect(self.bounds)
        self.action_LocalMesh.triggered.connect(self.view_local_mesh)
        self.action_RealMesh.triggered.connect(self.view_real_mesh)

        self.action_Orientation_Marker.triggered.connect(self.show_all_marker)
        self.action_log.triggered.connect(self.log_scalar)
        self.action_normal.triggered.connect(self.normal_scalar)
        self.action_ReverseXY.triggered.connect(self.view_reverse_xy)

        self.action_Clear.triggered.connect(self.clear)

        # menu Tools
        self.action_Threshold.triggered.connect(self.add_threshold)
        self.action_Crop.triggered.connect(self.cropping)
        self.signal_close.connect(self.plotter.close)
        # self.signal_close.connect(self.crop_win.close)

        # menu Add
        self.action_AddPoints.triggered.connect(self.add_points)
        self.action_AddLines.triggered.connect(self.add_lines)

        # Toolbar
        self.action_XOYview.triggered.connect(self.set_xoy_view)
        self.action_XOZview.triggered.connect(self.set_xoz_view)
        self.action_YOZview.triggered.connect(self.set_yoz_view)
        self.action_Isometric.triggered.connect(self.set_view_isometric)

    @track_error
    def get_config(self):
        self.config_type = 'VIEW'
        self.config_name = ['mesh_path', 'model_path',
                            'points_path', 'lines_path',
                            'window_width', 'window_height',
                            'window_pos_X', 'window_pos_y',
                            'showMaximized']
        init_variables = get_setting_values(self.config_type, self.config_name)
        self.label_MeshPath.setText(init_variables[0])
        self.label_ModelPath.setText(init_variables[1])
        self.points_path = init_variables[2]
        self.lines_path = init_variables[3]
        if init_variables[4]:
            self.resize(init_variables[4], init_variables[5])
        if init_variables[6]:
            self.move(init_variables[6], init_variables[7])
        if init_variables[8]:
            self.showMaximized()
        self.mesh_path = self.label_MeshPath.text()
        self.model_path = self.label_ModelPath.text()
        self.scalar_args = dict(title_font_size=20,
                                label_font_size=16,
                                vertical=True,
                                shadow=True,
                                position_x=0.9,
                                position_y=0.1,
                                height=0.8,
                                width=0.05)
                                # interactive=True)
        self.build_mesh_model()

    @track_error
    def load_mesh(self):
        self.mesh_path, _ = QFileDialog.getOpenFileName(self, 'Import mesh file',
                                                        self.label_MeshPath.text(),
                                                        '*.txt')
        if self.mesh_path:
            self.label_MeshPath.setText(self.mesh_path)
        self.build_mesh_model()

    @track_error
    def load_model(self):
        self.model_path, _ = QFileDialog.getOpenFileName(self, 'Import model file',
                                                         self.label_ModelPath.text(),
                                                         '*.txt')
        if self.model_path:
            self.label_ModelPath.setText(self.model_path)
        self.build_mesh_model()

    @track_error
    def build_mesh_model(self):
        if self.mesh_path:
            self.nodeX, self.nodeY, self.nodeZ = read_mesh_file(self.mesh_path)
            if self.model_path:
                self.model_in = np.loadtxt(self.model_path)
            if self.reverse_xy_flag:
                self.reverse_xy()
            self.add_mode = False
            self.grids = pv.MultiBlock()
            self.actors = []
            self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)

    @track_error
    def read_mesh_model(self):
        self.mesh_path, _ = QFileDialog.getOpenFileName(self, 'Import mesh file',
                                                        self.label_MeshPath.text(),
                                                        '*.txt')
        if self.mesh_path:
            self.model_path, _ = QFileDialog.getOpenFileName(self, 'Import model file',
                                                             self.label_ModelPath.text(),
                                                             '*.txt')
            if self.model_path:
                self.nodeX, self.nodeY, self.nodeZ = read_mesh_file(self.mesh_path)
                self.model_in = np.loadtxt(self.model_path)
                if self.reverse_xy_flag:
                    self.reverse_xy()
                self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
                # self.crop_win = CropModelDialog(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
                self.label_MeshPath.setText(self.mesh_path)
                self.label_ModelPath.setText(self.model_path)

    @track_error
    def display_model_pyvista(self):
        # self.plotter.clear()
        # self.plotter.set_background('white')
        self.add_mode = False
        self.grids = pv.MultiBlock()
        self.actors = []
        self.view_model_pyvista(self.nodeX, self.nodeY, self.nodeZ, self.model_in)

    @track_error
    def display_model_ubc(self):
        # self.plotter.clear()
        # self.plotter.set_background('white')
        self.add_mode = False
        self.grids = pv.MultiBlock()
        self.actors = []
        self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)

    @track_error_args
    def view_model_ubc(self, nodeX, nodeY, nodeZ, model_in):
        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ
        self.model_in = model_in
        self.ticks2grid(nodeX, nodeY, nodeZ)
        self.grids.append(self.grid)
        if model_in is None:
            if not self.add_mode:
                self.plotter.clear()
            else:
                # self.plotter.textActor.GetText(2)
                self.plotter.textActor.ClearAllTexts()
            self.actor = self.plotter.add_mesh(self.grid,
                                               style='wireframe')
            self.add_size_text()
            self.action_Threshold.setEnabled(False)
        else:
            if self.reverse_xy_flag:
                values = model_in.reshape((len(nodeX) - 1, len(nodeY) - 1, len(nodeZ) - 1)).transpose(1, 0, 2)
                values = values.flatten()
                values = values.reshape((len(nodeZ) - 1, len(nodeX) - 1, len(nodeY) - 1),
                                        order='F')
                self.grid.cell_arrays["values"] = values.flatten(order="C")
            else:
                values = model_in.reshape((len(nodeZ) - 1, len(nodeX) - 1, len(nodeY) - 1),
                                          order='F')
                self.grid.cell_arrays["values"] = values.flatten(order="C")
            if not self.add_mode:
                self.plotter.clear()
            else:
                self.plotter.textActor.ClearAllTexts()
            self.actor = self.plotter.add_mesh(self.grid,
                                               scalars='values',
                                               show_edges=True,
                                               scalar_bar_args=self.scalar_args)

            self.add_size_text()
            self.action_Threshold.setEnabled(True)

        self.actors.append(self.actor)
        self.bounds_flag = True
        self.bounds()

    @track_error_args
    def view_model_pyvista(self, nodeX, nodeY, nodeZ, model_in):
        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ
        self.model_in = model_in
        self.ticks2grid(nodeX, nodeY, nodeZ)
        self.grids.append(self.grid)
        if model_in is None:
            if not self.add_mode:
                self.plotter.clear()
            else:
                self.plotter.textActor.ClearAllTexts()
            self.actor = self.plotter.add_mesh(self.grid,
                                               style='wireframe')
            self.add_size_text()
            self.action_Threshold.setEnabled(False)
        else:
            self.grid.cell_arrays["values"] = model_in
            if not self.add_mode:
                self.plotter.clear()
            else:
                self.plotter.textActor.ClearAllTexts()
            self.actor = self.plotter.add_mesh(self.grid,
                                               scalars='values',
                                               show_edges=True,
                                               scalar_bar_args=self.scalar_args)
            self.add_size_text()
            self.action_Threshold.setEnabled(True)

        self.actors.append(self.actor)
        self.bounds_flag = True
        self.bounds()

    @track_error
    def load_mesh_model(self):
        self.add_mode = False
        self.grids = pv.MultiBlock()
        self.actors = []
        self.read_mesh_model()

    @track_error
    def add_mesh_model(self):
        self.add_mode = True
        self.read_mesh_model()

    @track_error_args
    def ticks2grid(self, node_x, node_y, node_z):
        if self.ticks == 'local':
            local_node_x = node_x - np.min(node_x)
            local_node_y = node_y - np.min(node_y)
            local_node_z = node_z - np.max(node_z)
            xx, yy, zz = np.meshgrid(local_node_x, local_node_y, local_node_z)
            self.grid = pv.StructuredGrid(xx, yy, zz)
        elif self.ticks == 'real':
            xx, yy, zz = np.meshgrid(node_x, node_y, node_z)
            self.grid = pv.StructuredGrid(xx, yy, zz)

    @track_error
    def view_local_mesh(self):
        self.ticks = 'local'
        self.set_view_isometric()
        self.display_model_ubc()

    @track_error
    def view_real_mesh(self):
        self.ticks = 'real'
        self.set_view_isometric()
        self.display_model_ubc()

    @track_error
    def reverse_xy(self):
        self.nodeX, self.nodeY = self.nodeY, self.nodeX

    @track_error
    def view_reverse_xy(self):
        if self.reverse_xy_flag:
            self.reverse_xy_flag = False
        else:
            self.reverse_xy_flag = True
        self.reverse_xy()
        self.add_mode = False
        self.grids = pv.MultiBlock()
        self.actors = []
        self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
        self.set_view_isometric()

    @track_error
    def add_size_text(self):
        x_range = np.max(self.nodeX) - np.min(self.nodeX)
        y_range = np.max(self.nodeY) - np.min(self.nodeY)
        z_range = np.max(self.nodeZ) - np.min(self.nodeZ)
        self.plotter.add_text('%.2f x %.2f x %.2f (%d x %d x %d)'
                              % (x_range, y_range, z_range,
                                 len(self.nodeX) - 1, len(self.nodeY) - 1, len(self.nodeZ) - 1),
                              position='upper_left',
                              font_size=14)

    @track_error
    def add_points(self):
        points_paths, _ = QFileDialog.getOpenFileNames(self,
                                                       "Choose points files",
                                                       self.points_path,
                                                       "*.txt")
        if points_paths:
            self.points_path = points_paths[0]
            for i in range(len(points_paths)):
                points_path = points_paths[i]
                points_o = np.loadtxt(points_path, delimiter=',')
                if self.reverse_xy_flag:
                    points_o[:, [0, 1]] = points_o[:, [1, 0]]
                points = pv.PolyData(points_o)
                self.plotter.add_points(points, color='k', point_size=6)

    @track_error
    def add_lines(self):
        points_paths, _ = QFileDialog.getOpenFileNames(self,
                                                       "Choose line points files",
                                                       self.lines_path,
                                                       "*.txt")
        if points_paths:
            self.points_path = points_paths[0]
            for i in range(len(points_paths)):
                points_path = points_paths[i]
                points = np.loadtxt(points_path, delimiter=',')
                if self.reverse_xy_flag:
                    points[:, [0, 1]] = points[:, [1, 0]]
                self.plotter.add_lines(points, color='b')

    @track_error
    def add_threshold(self):
        self.threshold_win = ThresholdDialog(self.model_in)
        self.threshold_win.show()
        self.threshold_win.signal.connect(self.cutoff)

    @track_error_args
    def cutoff(self, min_value, max_value):
        merged_grid = self.grids.combine()
        self.bounding_box_flag = False
        self.bounding_box()
        if self.log_flag:
            cutoff_gird = merged_grid.threshold(value=(min_value, max_value))
            for i in range(len(self.actors)):
                self.plotter.remove_actor(self.actors[i])
            self.actor = self.plotter.add_mesh(cutoff_gird,
                                               log_scale=True,
                                               scalar_bar_args=self.scalar_args)
            self.actors = [self.actor]
        else:
            cutoff_gird = merged_grid.threshold(value=(min_value, max_value),
                                                continuous=True)
            for i in range(len(self.actors)):
                self.plotter.remove_actor(self.actors[i])
            self.actor = self.plotter.add_mesh(cutoff_gird,
                                               scalar_bar_args=self.scalar_args)
            self.actors = [self.actor]
        self.bounds_flag = False
        self.bounds()

    @track_error
    def log_scalar(self):
        if not self.log_flag:
            self.plotter.clear()
            self.actor = self.plotter.add_mesh(self.grid,
                                               scalars='values',
                                               log_scale=True,
                                               show_edges=True,
                                               scalar_bar_args=self.scalar_args)
            self.log_flag = True

    @track_error
    def normal_scalar(self):
        if self.log_flag:
            self.plotter.clear()
            self.actor = self.plotter.add_mesh(self.grid,
                                               scalars='values',
                                               show_edges=True,
                                               scalar_bar_args=self.scalar_args)
            self.log_flag = False

    @track_error
    def cropping(self):
        self.crop_win = CropModelDialog(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
        self.crop_win.show()
        self.add_mode = False
        self.grids = pv.MultiBlock()
        self.actors = []
        self.crop_win.signal.connect(self.view_model_ubc)

    @track_error
    def wireframe(self):
        if self.model_flag:
            pass
        else:
            self.plotter.clear()
            self.actor = self.plotter.add_mesh(self.grid, style='wireframe')

    def bounding_box(self):
        if self.bounding_box_flag:
            self.plotter.remove_bounding_box()
            self.bounding_box_flag = False
        else:
            self.plotter.add_bounding_box()
            self.bounding_box_flag = True

    def bounds(self):
        if self.bounds_flag:
            self.plotter.show_bounds(grid='back', location='outer', all_edges=True)
            self.bounds_flag = False
        else:
            self.plotter.remove_bounds_axes()
            self.bounds_flag = True

    def show_all_marker(self):
        if self.orientation_marker_flag:
            self.plotter.hide_axes()
            self.orientation_marker_flag = False
        else:
            self.plotter.add_axes()
            self.orientation_marker_flag = True

    def set_xoy_view(self):
        self.plotter.view_xy()
        # self.plotter.view_yx()

    def set_xoz_view(self):
        self.plotter.view_xz()

    def set_yoz_view(self):
        self.plotter.view_yz()

    def set_view_isometric(self):
        self.plotter.view_isometric()

    def reset_camera(self):
        self.plotter.reset_camera()

    def closeEvent(self, event):
        variables = [self.label_MeshPath.text(), self.label_ModelPath.text(),
                     self.points_path, self.lines_path,
                     self.rect().width(), self.rect().height(),
                     self.pos().x(), self.pos().y(),
                     int(self.isMaximized())]
        set_setting_values(module_name=self.config_type, variable_names=self.config_name, variables=variables)
        self.plotter.clear()
        self.plotter.close()

    def clear(self):
        self.plotter.clear()
        self.add_mode = False
        self.grids = pv.MultiBlock()
        self.actors = []
