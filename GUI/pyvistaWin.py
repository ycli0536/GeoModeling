from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
from UI_init.Ui_ViewWin import Ui_MainWindow
from UI_init.Ui_CropModels import Ui_Dialog
from functions.utils import read_mesh_file, CellIndex2PointXYZ
from pyvistaqt import QtInteractor, MainWindow

import numpy as np
import pyvista as pv
import os


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


class CropModelDialog(QDialog, Ui_Dialog):
    signal = QtCore.pyqtSignal(np.ndarray, np.ndarray, np.ndarray, np.ndarray)

    def __init__(self, nodeX, nodeY, nodeZ, model_in):
        super(CropModelDialog, self).__init__()
        self.setupUi(self)
        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ
        self.model_in = model_in

        self.commandLinkBtn_datapath.setEnabled(False)
        self.commandLinkBtn_outputpath.setEnabled(False)
        self.label_datapath.setEnabled(False)
        self.label_outputpath.setEnabled(False)
        self.pushButton_crop.clicked.connect(self.crop)

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


class pyvistaWin(MainWindow, Ui_MainWindow):
    def __init__(self):
        super(pyvistaWin, self).__init__()
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.mesh_path = None
        self.model_path = None
        self.model_flag = True
        self.model_in = None
        self.bounding_box_flag = False
        self.bounds_flag = True
        self.log_flag = False
        self.orientation_marker_flag = False

        self.plotter = QtInteractor()
        self.verticalLayout.addWidget(self.plotter.interactor)

        # menu File
        self.action_Load.triggered.connect(self.load_mesh_model)
        self.commandLinkButton_mesh.clicked.connect(self.load_mesh)
        self.commandLinkButton_model.clicked.connect(self.load_model)

        # menu View
        self.action_PyVista.triggered.connect(self.display_model_pyvista)
        self.action_UBC.triggered.connect(self.display_model_ubc)
        self.action_Wireframe.triggered.connect(self.wireframe)
        self.action_BoundingBox.triggered.connect(self.bounding_box)
        self.action_Bounds.triggered.connect(self.bounds)
        self.action_Orientation_Marker.triggered.connect(self.show_all_marker)
        self.action_log.triggered.connect(self.log_scalar)
        self.action_normal.triggered.connect(self.normal_scalar)

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
    def load_mesh(self):
        self.mesh_path, _ = QFileDialog.getOpenFileName(self, 'Import mesh file', '.\\', '*.txt')
        if self.mesh_path:
            self.label_MeshPath.setText(self.mesh_path)
            self.nodeX, self.nodeY, self.nodeZ = read_mesh_file(self.mesh_path)
            self.action_Threshold.setEnabled(True)
        self.build_mesh_model()

    @track_error
    def load_model(self):
        self.model_path, _ = QFileDialog.getOpenFileName(self, 'Import model file', '.\\', '*.txt')
        if self.model_path:
            self.label_ModelPath.setText(self.model_path)
            self.model_in = np.loadtxt(self.model_path)
            self.action_Threshold.setEnabled(True)
        self.build_mesh_model()
            
    @track_error
    def build_mesh_model(self):
        if self.mesh_path:
            self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)

    @track_error
    def load_mesh_model(self):
        self.mesh_path, _ = QFileDialog.getOpenFileName(self, 'Import mesh file', '.\\', '*.txt')
        if self.mesh_path:
            self.model_path, _ = QFileDialog.getOpenFileName(self, 'Import model file', '.\\', '*.txt')
            if self.model_path:
                self.nodeX, self.nodeY, self.nodeZ = read_mesh_file(self.mesh_path)
                self.model_in = np.loadtxt(self.model_path)
                self.action_Threshold.setEnabled(True)
                self.plotter.clear()
                self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
                # self.crop_win = CropModelDialog(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
                self.label_MeshPath.setText(self.mesh_path)
                self.label_ModelPath.setText(self.model_path)

    @track_error
    def display_model_pyvista(self):
        # self.plotter.clear()
        # self.plotter.set_background('white')
        self.view_model_pyvista(self.nodeX, self.nodeY, self.nodeZ, self.model_in)

    @track_error
    def display_model_ubc(self):
        # self.plotter.clear()
        # self.plotter.set_background('white')
        self.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_in)

    @track_error_args
    def view_model_ubc(self, nodeX, nodeY, nodeZ, model_in):
        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ
        self.model_in = model_in
        xx, yy, zz = np.meshgrid(nodeX, nodeY, nodeZ)
        self.grid = pv.StructuredGrid(xx, yy, zz)
        if model_in is None:
            self.plotter.clear()
            self.plotter.add_mesh(self.grid,
                                  style='wireframe')
            self.add_size_text()
            self.action_Threshold.setEnabled(False)
        else:
            self.plotter.clear()
            values = model_in.reshape((len(nodeZ) - 1, len(nodeX) - 1, len(nodeY) - 1),
                                      order='F')
            self.grid.cell_arrays["values"] = values.flatten(order="C")
            self.plotter.add_mesh(self.grid,
                                  scalars='values',
                                  show_edges=True)
            self.add_size_text()

        self.bounds_flag = True
        self.bounds()

    @track_error_args
    def view_model_pyvista(self, nodeX, nodeY, nodeZ, model_in):
        self.nodeX = nodeX
        self.nodeY = nodeY
        self.nodeZ = nodeZ
        self.model_in = model_in
        xx, yy, zz = np.meshgrid(nodeX, nodeY, nodeZ)
        self.grid = pv.StructuredGrid(xx, yy, zz)
        if model_in is None:
            self.plotter.clear()
            self.plotter.add_mesh(self.grid,
                                  style='wireframe')
            self.add_size_text()
            self.action_Threshold.setEnabled(False)
        else:
            self.grid.cell_arrays["values"] = model_in
            self.plotter.clear()
            self.plotter.add_mesh(self.grid,
                                  scalars='values',
                                  show_edges=True)
            self.add_size_text()

        self.bounds_flag = True
        self.bounds()

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
                                                       "*.txt")
        if points_paths:
            for i in range(len(points_paths)):
                points_path = points_paths[i]
                points_o = np.loadtxt(points_path, delimiter=',')
                points = pv.PolyData(points_o)
                self.plotter.add_points(points, color='y', point_size=6)

    @track_error
    def add_lines(self):
        points_paths, _ = QFileDialog.getOpenFileNames(self,
                                                       "Choose line points files",
                                                       "*.txt")
        if points_paths:
            for i in range(len(points_paths)):
                points_path = points_paths[i]
                points = np.loadtxt(points_path, delimiter=',')
                self.plotter.add_lines(points, color='b')

    @track_error
    def add_threshold(self):
        self.plotter.clear()
        # # self.plotter.add_mesh(self.grid,
        # #                       scalars='values',
        # #                       opacity=0.3,
        # #                       #   nan_opacity=0,
        # #                       categories=True,
        # #                       show_edges=False)
        if self.log_flag:
            self.plotter.add_mesh_threshold(self.grid,
                                            invert=False,
                                            log_scale=True)
        else:
            self.plotter.add_mesh_threshold(self.grid,
                                            invert=False)
        self.bounds_flag = True
        self.bounds()

        # print(type(threshed))

        # grid_target = self.grid.cast_to_unstructured_grid()
        # ghosts = np.argwhere(grid_target["values"] == self.val)
        # grid_target.remove_cells(ghosts)
        # self.plotter.add_mesh(grid_target,
        #                       scalars='values',
        #                       # log_scale=True,
        #                       # opacity=1,
        #                       show_edges=True)

    @track_error
    def log_scalar(self):
        if not self.log_flag:
            self.plotter.clear()
            self.plotter.add_mesh(self.grid,
                                  scalars='values',
                                  log_scale=True,
                                  show_edges=True)
            self.log_flag = True

    @track_error
    def normal_scalar(self):
        if self.log_flag:
            self.plotter.clear()
            self.plotter.add_mesh(self.grid,
                                  scalars='values',
                                  show_edges=True)
            self.log_flag = False

    @track_error
    def cropping(self):
        self.crop_win = CropModelDialog(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
        self.crop_win.show()
        self.crop_win.signal.connect(self.view_model_ubc)

    @track_error
    def wireframe(self):
        if self.model_flag:
            pass
        else:
            self.plotter.clear()
            self.plotter.add_mesh(self.grid, style='wireframe')

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
        self.plotter.clear()
        self.plotter.close()

    def clear(self):
        self.plotter.clear()
