from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem, QComboBox
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from pyvistaqt import QtInteractor
import pyvista as pv

from UI_init.Ui_tabMesh import Ui_tab_mesh as Ui_TabMesh

from GUI.FilenameSetting import FileNameSettingWin

from functions.AutoPadding import auto_padding
from functions.utils import write_mesh_file

import numpy as np
import os


def track_error(func):
    def wrapper(self):
        try:
            func(self)
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def finished_reminder(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        QMessageBox.information(self, 'Finished', 'Task finished.', QMessageBox.Yes)
    return wrapper


class AddTabMesh(QTabWidget, Ui_TabMesh):
    def __init__(self, path):
        super(AddTabMesh, self).__init__()
        self.setupUi(self)
        self.project_dir = path

        self.nodeX = None
        self.nodeY = None
        self.nodeZ = None

        self.core_Volume = None
        self.dx = None
        self.dy = None
        self.dz = None

        self.padding_rateX = None
        self.padding_rateY = None
        self.padding_rateZ = None

        self.padding_rangeX = None
        self.padding_rangeY = None
        self.padding_rangeZ = None

        self.plotter = QtInteractor(self.groupBox_ViewMesh)
        self.verticalLayout_view.addWidget(self.plotter.interactor)

        self.pushButton_ViewMesh.clicked.connect(self.view_mesh)
        self.pushButton_SaveMesh.clicked.connect(self.save_mesh)

    @track_error
    def view_mesh(self):
        self.get_parameters()
        self.plotter.clear()
        xx, yy, zz = np.meshgrid(self.nodeX, self.nodeY, self.nodeZ)
        grid = pv.StructuredGrid(xx, yy, zz)
        self.plotter.add_mesh(grid, style='wireframe')
        self.plotter.add_bounding_box()
        self.plotter.show_bounds(grid='front', location='outer', all_edges=True)
        self.plotter.add_axes()

    @track_error
    def save_mesh(self):
        # flag = True
        # try:
        #     self.get_parameters()
        # except:
        #     flag = False

        # if flag:
        self.get_parameters()
        save_win = FileNameSettingWin()
        project_name = self.project_dir.split('/')[-1]
        save_win.label_path.setText('%s/Mesh/' % project_name)
        save_win.label_filename.setText('Mesh filename: ')
        save_win.exec()

        if save_win.create_flag:
            mesh_filename = save_win.lineEdit_filename.text() + '.txt'
            mesh_path = os.path.join(self.project_dir, *['Mesh', mesh_filename])
            self.write_mesh_file(mesh_path=mesh_path)

    # @track_error
    @finished_reminder
    def write_mesh_file(self, mesh_path):
        write_mesh_file(mesh_path=mesh_path,
                        nodeX=self.nodeX,
                        nodeY=self.nodeY,
                        nodeZ=self.nodeZ)

    @track_error
    def get_parameters(self):
        Xcore = [float(self.lineEdit_Xmin.text()), float(self.lineEdit_Xmax.text())]
        Ycore = [float(self.lineEdit_Ymin.text()), float(self.lineEdit_Ymax.text())]
        Zcore = [float(self.lineEdit_Zmin.text()), float(self.lineEdit_Zmax.text())]

        dx = float(self.lineEdit_dx.text())
        dy = float(self.lineEdit_dy.text())
        dz = float(self.lineEdit_dz.text())

        Xpadding_rate = float(self.lineEdit_XpaddingR.text())
        Ypadding_rate = float(self.lineEdit_YpaddingR.text())
        Zpadding_rate = float(self.lineEdit_ZpaddingR.text())

        Xpadding = [float(self.lineEdit_Xpaddingmin.text()), float(self.lineEdit_Xpaddingmax.text())]
        Ypadding = [float(self.lineEdit_Ypaddingmin.text()), float(self.lineEdit_Ypaddingmax.text())]
        Zpadding = [float(self.lineEdit_Zpaddingmin.text()), float(self.lineEdit_Zpaddingmax.text())]

        self.nodeX, self.nodeY, self.nodeZ = auto_padding(Xcore=Xcore, dx=dx, Xpadding_rate=Xpadding_rate, Xpadding=Xpadding,
                                                          Ycore=Ycore, dy=dy, Ypadding_rate=Ypadding_rate, Ypadding=Ypadding,
                                                          Zcore=Zcore, dz=dz, Zpadding_rate=Zpadding_rate, Zpadding=Zpadding)
