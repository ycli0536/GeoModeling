from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog

from UI_init.Ui_CropModels import Ui_Dialog
from functions.utils import CellIndex2PointXYZ
from functions.utils import write_mesh_file

import os
import numpy as np
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


class CropModelDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(CropModelDialog, self).__init__()
        self.setupUi(self)

        self.commandLinkBtn_datapath.clicked.connect(self.get_root_path)
        self.commandLinkBtn_outputpath.clicked.connect(self.get_output_path)
        self.pushButton_crop.clicked.connect(self.crop)

    @track_error
    def get_root_path(self):
        self.rootpath = QFileDialog.getExistingDirectory(self,
                                                         "Select a exported folder",
                                                         "./")
        if self.rootpath:
            self.commandLinkBtn_datapath.setText(self.rootpath)

    @track_error
    def get_output_path(self):
        self.output_folder = QFileDialog.getExistingDirectory(self,
                                                              "Select a folder",
                                                              "./")
        if self.output_folder:
            outputpath = os.path.join(self.output_folder, 'output')
            self.commandLinkBtn_outputpath.setText(outputpath)

    @track_error
    def crop(self):
        try:
            if os.path.exists(self.commandLinkBtn_outputpath.text()):
                shutil.rmtree(self.commandLinkBtn_outputpath.text())
            os.mkdir(self.commandLinkBtn_outputpath.text())

            subfolders = os.listdir(self.commandLinkBtn_datapath.text())
            nodeX = np.loadtxt(os.path.join(self.rootpath, *[subfolders[0], 'nodeX.txt']))
            nodeY = np.loadtxt(os.path.join(self.rootpath, *[subfolders[0], 'nodeY.txt']))
            nodeZ = np.loadtxt(os.path.join(self.rootpath, *[subfolders[0], 'nodeZ.txt']))

            xmin = float(self.lineEdit_Xmin.text())
            xmax = float(self.lineEdit_Xmax.text())
            assert nodeX[0] < xmin < xmax < nodeX[-1]

            ymin = float(self.lineEdit_Ymin.text())
            ymax = float(self.lineEdit_Ymax.text())
            assert nodeY[0] < ymin < ymax < nodeY[-1]

            zmin = float(self.lineEdit_Zmin.text())
            zmax = float(self.lineEdit_Zmax.text())
            assert nodeZ[-1] < zmin < zmax < nodeZ[0]

            indx = (xmin <= nodeX) & (xmax >= nodeX)
            indy = (ymin <= nodeY) & (ymax >= nodeY)
            indz = (zmin <= nodeZ) & (zmax >= nodeZ)

            sub_nodeX = nodeX[indx]
            sub_nodeY = nodeY[indy]
            sub_nodeZ = nodeZ[indz]

            sub_mesh_path = os.path.join(self.commandLinkBtn_outputpath.text(), 'sub_mesh.txt')
            write_mesh_file(mesh_path=sub_mesh_path,
                            nodeX=sub_nodeX,
                            nodeY=sub_nodeY,
                            nodeZ=sub_nodeZ)

            temp = CellIndex2PointXYZ(nodeX, nodeY, nodeZ, [])
            x = temp[:, 0]
            y = temp[:, 1]
            z = temp[:, 2]

            # model_out = np.empty((len(subfolders), len(sub_nodeY) - 1, len(sub_nodeX) - 1, len(sub_nodeZ) - 1))
            for i in range(len(subfolders)):
                # original model vector -> cropped model vector -> cropped model matrix
                cropped_model = np.empty((len(sub_nodeY) - 1, len(sub_nodeX) - 1, len(sub_nodeZ) - 1))
                model_o = np.loadtxt(os.path.join(self.rootpath, *[subfolders[i], 'cellCon.txt']))

                ind = (x >= sub_nodeX[0]) & (x <= sub_nodeX[-1]) & \
                      (y >= sub_nodeY[0]) & (y <= sub_nodeY[-1]) & \
                      (z <= sub_nodeZ[0]) & (z >= sub_nodeZ[-1])
                cropped_model_o = model_o[ind]
                # UBC format: Z, X, Y
                values = cropped_model_o.reshape((len(sub_nodeZ) - 1, len(sub_nodeX) - 1, len(sub_nodeY) - 1),
                                                 order='F')
                for j in range(len(sub_nodeZ) - 1):
                    cropped_model[:, :, j] = values[j, :, :].T

                np.save(os.path.join(self.commandLinkBtn_outputpath.text(), 'cropped_model_%05d' % i), cropped_model)

                # # original model vector -> original model matrix -> cropped model matrix
                # cropped_model = np.empty((len(sub_nodeY) - 1, len(sub_nodeX) - 1, len(sub_nodeZ) - 1))
                # model_o = np.loadtxt(os.path.join(self.rootpath, *[subfolders[i], 'cellCon.txt']))
                # # UBC format: Z, X, Y
                # values = model_o.reshape((len(nodeZ) - 1, len(nodeX) - 1, len(nodeY) - 1),
                #                          order='F')
                #
                # model = np.empty((len(nodeY) - 1, len(nodeX) - 1, len(nodeZ) - 1))
                # for j in range(len(nodeZ) - 1):
                #     model[:, :, j] = values[j, :, :].T
                #
                # cropped_model = model[np.where(indy)[0][0]:np.where(indy)[0][-1],
                #                       np.where(indx)[0][0]:np.where(indx)[0][-1],
                #                       np.where(indz)[0][0]:np.where(indz)[0][-1]]
                #
                # np.save(os.path.join(self.commandLinkBtn_outputpath.text(), 'cropped_model_%05d' % i), cropped_model)
            QMessageBox.information(self.pushButton_crop,
                                    'Model Cropping',
                                    'Model (%d*%d*%d [YXZ]) is cropped.' % (len(sub_nodeY) - 1,
                                                                            len(sub_nodeX) - 1,
                                                                            len(sub_nodeZ) - 1),
                                    QMessageBox.Yes)

        except AssertionError:
            QMessageBox.warning(self.pushButton_crop,
                                "Error",
                                "Pleas set right sub-space!",
                                QMessageBox.Yes)
