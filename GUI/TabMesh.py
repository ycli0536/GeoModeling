from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem, QComboBox
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from pyvistaqt import QtInteractor
import pyvista as pv

from UI_init.Ui_tabMesh import Ui_tab_mesh as Ui_TabMesh

from GUI.FilenameSetting import FileNameSettingWin

from functions.AutoPadding import auto_padding
from functions.utils import write_mesh_file
from functions.decorators import track_error, track_error_args, finished_reminder
from functions.config_setting import get_setting_values, set_setting_values

import numpy as np
import os


class AddTabMesh(QTabWidget, Ui_TabMesh):
    def __init__(self, path):
        super(AddTabMesh, self).__init__()
        self.setupUi(self)
        self.get_config()
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
    def get_config(self):
        self.config_type = 'MESH'
        self.config_name = ['x_core_min', 'x_core_max',
                            'y_core_min', 'y_core_max',
                            'z_core_min', 'z_core_max',
                            'dx', 'dy', 'dz',
                            'x_rate', 'y_rate', 'z_rate',
                            'x_padding_min', 'x_padding_max',
                            'y_padding_min', 'y_padding_max',
                            'z_padding_min', 'z_padding_max']
        init_variables = get_setting_values(self.config_type, self.config_name)
        self.lineEdit_Xmin.setText(init_variables[0])
        self.lineEdit_Xmax.setText(init_variables[1])
        self.lineEdit_Ymin.setText(init_variables[2])
        self.lineEdit_Ymax.setText(init_variables[3])
        self.lineEdit_Zmin.setText(init_variables[4])
        self.lineEdit_Zmax.setText(init_variables[5])

        self.lineEdit_dx.setText(init_variables[6])
        self.lineEdit_dy.setText(init_variables[7])
        self.lineEdit_dz.setText(init_variables[8])

        self.lineEdit_XpaddingR.setText(init_variables[9])
        self.lineEdit_YpaddingR.setText(init_variables[10])
        self.lineEdit_ZpaddingR.setText(init_variables[11])

        self.lineEdit_Xpaddingmin.setText(init_variables[12])
        self.lineEdit_Xpaddingmax.setText(init_variables[13])
        self.lineEdit_Ypaddingmin.setText(init_variables[14])
        self.lineEdit_Ypaddingmax.setText(init_variables[15])
        self.lineEdit_Zpaddingmin.setText(init_variables[16])
        self.lineEdit_Zpaddingmax.setText(init_variables[17])

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

    # @track_error_args
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

    @track_error
    def tab_removed(self):
        variables = [self.lineEdit_Xmin.text(), self.lineEdit_Xmax.text(),
                     self.lineEdit_Ymin.text(), self.lineEdit_Ymax.text(),
                     self.lineEdit_Zmin.text(), self.lineEdit_Zmax.text(),
                     self.lineEdit_dx.text(), self.lineEdit_dy.text(), self.lineEdit_dz.text(),
                     self.lineEdit_XpaddingR.text(), self.lineEdit_YpaddingR.text(), self.lineEdit_ZpaddingR.text(),
                     self.lineEdit_Xpaddingmin.text(), self.lineEdit_Xpaddingmax.text(),
                     self.lineEdit_Ypaddingmin.text(), self.lineEdit_Ypaddingmax.text(),
                     self.lineEdit_Zpaddingmin.text(), self.lineEdit_Zpaddingmax.text()]
        set_setting_values(module_name=self.config_type, variable_names=self.config_name, variables=variables)
