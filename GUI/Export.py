from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from UI_init.Ui_Export import Ui_Dialog

from functions.utils import read_mesh_file
from functions.decorators import track_error, track_error_args
from functions.config_setting import get_setting_values, set_setting_values

import os
import numpy as np
import shutil


class ExportDialog(QDialog, Ui_Dialog):
    def __init__(self, path):
        super(ExportDialog, self).__init__()
        self.setupUi(self)
        self.get_config()
        self.project_dir = path
        self.select_flag = False

        self.show_dirs()

        self.pushBtn_frqbrowser.clicked.connect(self.load_frq)
        self.pushButton_ok.clicked.connect(self.export)

    @track_error
    def get_config(self):
        self.config_type = 'EXPORT'
        self.config_name = ['frq_path',
                            'window_width', 'window_height',
                            'window_pos_x', 'window_pos_y',]
        init_variables = get_setting_values(self.config_type, self.config_name)
        self.frq_path = init_variables[0]
        self.lineEdit_frq.setText(self.frq_path)
        if init_variables[1]:
            self.resize(init_variables[1], init_variables[2])
        if init_variables[3]:
            self.move(init_variables[3], init_variables[4])

    @track_error
    def load_frq(self):
        self.frq_path, _ = QFileDialog.getOpenFileName(self, "Import frequency file", ".txt")
        if self.frq_path:
            self.lineEdit_frq.setText(self.frq_path)

    @track_error
    def show_dirs(self):
        self.mesh_path = os.path.join(self.project_dir, "Mesh")
        self.src_path = os.path.join(self.project_dir, *["Survey", "Source"])
        self.rcv_path = os.path.join(self.project_dir, *["Survey", "Receiver"])
        self.wellpath_path = os.path.join(self.project_dir, "Wellpath")

        mesh_dir = os.listdir(self.mesh_path)
        src_dir = os.listdir(self.src_path)
        rcv_dir = os.listdir(self.rcv_path)
        wellpath_dir = os.listdir(self.wellpath_path)

        self.listWidget_mesh.addItems(mesh_dir)
        self.listWidget_src.addItems(src_dir)
        self.listWidget_rcv.addItems(rcv_dir)
        self.listWidget_well.addItems(wellpath_dir)

    # @track_error
    def get_paths(self):
        if self.listWidget_mesh.selectedItems() and \
           self.listWidget_src.selectedItems() and \
           self.listWidget_rcv.selectedItems() and \
           self.listWidget_well.selectedItems():

            mesh_filename = self.listWidget_mesh.selectedItems()[0].text()
            self.mesh_file = os.path.join(self.mesh_path, mesh_filename)
            src_filename = self.listWidget_src.selectedItems()[0].text()
            self.src_file = os.path.join(self.src_path, src_filename)
            rcv_filename = self.listWidget_rcv.selectedItems()[0].text()
            self.rcv_file = os.path.join(self.rcv_path, rcv_filename)
            wellpath_filename = self.listWidget_well.selectedItems()[0].text()
            self.wellpath_file = os.path.join(self.wellpath_path, wellpath_filename)
            self.select_flag = True
        else:
            QMessageBox.warning(self, 'Warning',
                                'You have not select all files!',
                                QMessageBox.Yes)

    # @track_error
    def export(self):
        foldername = QFileDialog.getExistingDirectory(self, "Select a folder", "./")
        if foldername:
            filename = os.path.join(foldername, "export")
            self.get_paths()
            if self.select_flag:

                if os.path.exists(filename):
                    shutil.rmtree(filename)

                # create sub folder for each model
                model_path = os.path.join(self.project_dir, "Model")
                os.mkdir(filename)
                for i, model_file in enumerate(os.listdir(model_path)):
                    tmp = os.path.join(filename, str(i + 1))
                    os.mkdir(tmp)
                    original_model_path = os.path.join(model_path, model_file)

                    nodex_save_path = os.path.join(tmp, 'nodeX.txt')
                    nodey_save_path = os.path.join(tmp, 'nodeY.txt')
                    nodez_save_path = os.path.join(tmp, 'nodeZ.txt')

                    rcv_save_path = os.path.join(tmp, 'rcvPath.txt')
                    src_save_path = os.path.join(tmp, 'srcPath.txt')

                    model_save_path = os.path.join(tmp, 'cellCon.txt')
                    wellpath_save_path = os.path.join(tmp, 'edgeCon.txt')

                    frq_save_path = os.path.join(tmp, 'frqFile')

                    nodeX, nodeY, nodeZ = read_mesh_file(mesh_path=self.mesh_file)

                    # save nodeX, nodeY, and nodeZ
                    nodeY = np.round(nodeY, 3)
                    nodeZ = np.round(nodeZ, 3)
                    nodeX = np.round(nodeX, 3)
                    with open(nodex_save_path, 'w') as f:
                        for k in range(len(nodeX)):
                            f.write(str(float(nodeX[k])) + "\n")
                    with open(nodey_save_path, 'w') as f:
                        for k in range(len(nodeY)):
                            f.write(str(float(nodeY[k])) + "\n")
                    with open(nodez_save_path, 'w') as f:
                        for k in range(len(nodeZ)):
                            f.write(str(float(nodeZ[k])) + "\n")

                    # save cellCon (model)
                    shutil.copy(original_model_path, model_save_path)

                    # save receiver config
                    shutil.copy(self.rcv_file, rcv_save_path)

                    # save source config
                    shutil.copy(self.src_file, src_save_path)
                    # with open(src_save_path, 'w') as f:

                    # save edgeCon (wellpath)
                    shutil.copy(self.wellpath_file, wellpath_save_path)

                    # save frqFile
                    shutil.copy(self.frq_path, frq_save_path)

                QMessageBox.information(self.pushButton_ok,
                                        'Information',
                                        'Export complete!',
                                        QMessageBox.Yes)
                self.close()

    @track_error_args
    def closeEvent(self, event):
        variables = [self.lineEdit_frq.text(),
                     self.rect().width(), self.rect().height(),
                     self.pos().x(), self.pos().y()]
        set_setting_values(module_name=self.config_type, variable_names=self.config_name, variables=variables)
        if not self.select_flag:
            reply = QMessageBox.question(self, 'Discard?',
                                         'Discard this operation?',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
