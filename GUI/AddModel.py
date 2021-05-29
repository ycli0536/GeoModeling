from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore

from functions.addModels import addModels
from functions.utils import read_mesh_file

from UI_init.Ui_addSlab import Ui_Dialog as SlabDialog
from UI_init.Ui_addEllipsoid import Ui_Dialog as EllipsoidDialog
from UI_init.Ui_addRandomEllipsoid import Ui_Dialog as RandomEllipsoidDialog
from UI_init.Ui_addRandomSlab import Ui_Dialog as RandomSlabDialog
from UI_init.Ui_progressWin import Ui_Dialog as ProgressDialog

from GUI.FilenameSetting import FileNameSettingWin
from GUI.SelectWin import SelectWin
from GUI.pyvistaWin import pyvistaWin

from functools import partial
import numpy as np
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
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            QMessageBox.information(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


class GenerationWorker(QtCore.QObject):
    no_dir_signal = QtCore.pyqtSignal()
    on_each_loop_end_signal = QtCore.pyqtSignal(int)
    start_random_gen = QtCore.pyqtSignal()
    finish_random_gen = QtCore.pyqtSignal()

    def __init__(self):
        super(GenerationWorker, self).__init__()

    @track_error_args
    def ellipsoid_random_gen(self, project_dir, model_count,
                             nodeX, nodeY, nodeZ, model_in,
                             centerX_set, centerY_set, centerZ_set,
                             R_alpha_set, R_beta_set, R_theta_set,
                             a_xis_set, b_xis_set, c_xis_set,
                             val_set):
        self.start_random_gen.emit()
        for i in range(model_count):
            # save as ...
            model_filename = 'model' + str(i + 1) + '.txt'
            dir = os.path.join(project_dir, *["Model", model_filename])
            if dir:
                models = addModels(nodeX, nodeY, nodeZ, model_in)
                model_out = models.addEllipsoid([centerX_set[i], centerY_set[i], centerZ_set[i]],
                                                [R_alpha_set[i], R_beta_set[i], R_theta_set[i]],
                                                [a_xis_set[i], b_xis_set[i], c_xis_set[i]],
                                                val_set[i])

                with open(dir, 'w') as f:
                    for k in range(len(model_out)):
                        f.write(str(float(model_out[k])) + "\n")
            else:
                self.no_dir_signal.emit()
                break
            self.on_each_loop_end_signal.emit(i)

        config_filename = 'config.txt'
        config_dir = os.path.join(project_dir, config_filename)
        with open(config_dir, 'w') as writer:
            writer.write('ID, VAL, CENTER_X, CENTER_Y, CENTER_Z, R_ALPHA(°), R_BETA(°), R_THETA(°), ')
            writer.write('AXIS_X, AXIS_Y, AXIS_Z\n')
            for sample_id in range(len(val_set)):
                writer.write('%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n'
                             % (sample_id + 1,
                                val_set[sample_id],
                                centerX_set[sample_id],
                                centerY_set[sample_id],
                                centerZ_set[sample_id],
                                R_alpha_set[sample_id] * 180 / np.pi,
                                R_beta_set[sample_id] * 180 / np.pi,
                                R_theta_set[sample_id] * 180 / np.pi,
                                a_xis_set[sample_id],
                                b_xis_set[sample_id],
                                c_xis_set[sample_id]))

        self.finish_random_gen.emit()

    @track_error_args
    def slab_random_gen(self, project_dir, model_count, normal,
                        nodeX, nodeY, nodeZ, model_in,
                        ControlLength_Set,
                        SlabcenterX_Set, SlabcenterY_Set, SlabcenterZ_Set,
                        SlabRalpha_Set, SlabRbeta_Set, SlabRtheta_Set,
                        SlabVal_Set, SlabTh_Set):
        self.start_random_gen.emit()
        for i in range(model_count):
            # save as ...
            model_filename = 'model' + str(i + 1) + '.txt'
            dir = os.path.join(project_dir, *["Model", model_filename])
            if dir:
                models = addModels(nodeX, nodeY, nodeZ, model_in)
                sfLocInfo = self.slab_control_points(ControlLength_Set[:, i],
                                                     [SlabcenterX_Set[i], SlabcenterY_Set[i], SlabcenterZ_Set[i]],
                                                     [SlabRalpha_Set[i], SlabRbeta_Set[i], SlabRtheta_Set[i]], normal)
                model_out = models.addSlab(sfLocInfo, SlabTh_Set[i], SlabVal_Set[i], normal)

                with open(dir, 'w') as f:
                    for k in range(len(model_out)):
                        f.write(str(float(model_out[k])) + "\n")

                # save sfLocInfo to config_points.txt
                config_points_filename = 'config_points.txt'
                config_points_dir = os.path.join(project_dir, config_points_filename)
                if i == 0:
                    with open(config_points_dir, 'w') as writer:
                        writer.write('ID, LOC_DIM1, LOC_DIM2, LOC_DIM3\n')
                with open(config_points_dir, 'a') as writer:
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[0][0], sfLocInfo[0][1], sfLocInfo[0][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[1][0], sfLocInfo[1][1], sfLocInfo[1][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[2][0], sfLocInfo[2][1], sfLocInfo[2][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[3][0], sfLocInfo[3][1], sfLocInfo[3][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[4][0], sfLocInfo[4][1], sfLocInfo[4][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[5][0], sfLocInfo[5][1], sfLocInfo[5][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[6][0], sfLocInfo[6][1], sfLocInfo[6][2]))
                    writer.write('%d, %f, %f, %f\n' % (i + 1, sfLocInfo[7][0], sfLocInfo[7][1], sfLocInfo[7][2]))
            else:
                self.no_dir_signal.emit()
                break
            self.on_each_loop_end_signal.emit(i)

        config_filename = 'config.txt'
        config_dir = os.path.join(project_dir, config_filename)
        with open(config_dir, 'w') as writer:
            writer.write('ID, THICKNESS, VAL, CENTER_X, CENTER_Y, CENTER_Z, R_ALPHA(°), R_BETA(°), R_THETA(°), ')
            writer.write('LEN_0, LEN_45, LEN_90, LEN_135, LEN_180, LEN_225, LEN_270, LEN_315\n')
            for sample_id in range(len(SlabVal_Set)):
                writer.write('%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n'
                             % (sample_id + 1,
                                SlabTh_Set[sample_id],
                                SlabVal_Set[sample_id],
                                SlabcenterX_Set[sample_id],
                                SlabcenterY_Set[sample_id],
                                SlabcenterZ_Set[sample_id],
                                SlabRalpha_Set[sample_id] * 180 / np.pi,
                                SlabRbeta_Set[sample_id] * 180 / np.pi,
                                SlabRtheta_Set[sample_id] * 180 / np.pi,
                                ControlLength_Set[0, sample_id],
                                ControlLength_Set[1, sample_id],
                                ControlLength_Set[2, sample_id],
                                ControlLength_Set[3, sample_id],
                                ControlLength_Set[4, sample_id],
                                ControlLength_Set[5, sample_id],
                                ControlLength_Set[6, sample_id],
                                ControlLength_Set[7, sample_id]))

        self.finish_random_gen.emit()

    @track_error_args
    def slab_control_points(self, ControlLengths, CenterPoints, R_Angles, normal):
        Yp = ControlLengths[0]
        Yn = ControlLengths[1]
        Xp = ControlLengths[2]
        Xn = ControlLengths[3]
        XpYp = ControlLengths[4]
        XpYn = ControlLengths[5]
        XnYp = ControlLengths[6]
        XnYn = ControlLengths[7]
        SlabcenterX = CenterPoints[0]
        SlabcenterY = CenterPoints[1]
        SlabcenterZ = CenterPoints[2]
        center = np.array([SlabcenterX, SlabcenterY, SlabcenterZ])
        Slabalpha = R_Angles[0] * np.pi / 180
        Slabbeta = R_Angles[1] * np.pi / 180
        Slabtheta = R_Angles[2] * np.pi / 180

        R_matrix = [[np.cos(Slabtheta) * np.cos(Slabbeta),
                     - np.sin(Slabtheta) * np.cos(Slabalpha) + np.cos(Slabtheta) * np.sin(Slabbeta) * np.sin(Slabalpha),
                     np.sin(Slabtheta) * np.sin(Slabalpha) + np.cos(Slabtheta) * np.sin(Slabbeta) * np.cos(Slabalpha)],
                    [np.sin(Slabtheta) * np.cos(Slabbeta),
                     np.cos(Slabtheta) * np.cos(Slabalpha) + np.sin(Slabtheta) * np.sin(Slabbeta) * np.sin(Slabalpha),
                     - np.cos(Slabtheta) * np.sin(Slabalpha) + np.sin(Slabtheta) * np.sin(Slabbeta) * np.cos(
                         Slabalpha)],
                    [- np.sin(Slabbeta), np.cos(Slabbeta) * np.sin(Slabalpha), np.cos(Slabbeta) * np.cos(Slabalpha)]
                    ]
        # clockwise
        if normal == 'z':
            SlabShape_origin = [[0, Yp, 0], [np.sqrt(2) / 2 * XpYp, np.sqrt(2) / 2 * XpYp, 0],
                                [Xp, 0, 0], [np.sqrt(2) / 2 * XpYn, - np.sqrt(2) / 2 * XpYn, 0],
                                [0, - Yn, 0], [- np.sqrt(2) / 2 * XnYn, - np.sqrt(2) / 2 * XnYn, 0],
                                [- Xn, 0, 0], [- np.sqrt(2) / 2 * XnYp, np.sqrt(2) / 2 * XnYp, 0]
                                ]
        if normal == 'y':
            SlabShape_origin = [[0, 0, Yp], [np.sqrt(2) / 2 * XpYp, 0, np.sqrt(2) / 2 * XpYp],
                                [Xp, 0, 0], [np.sqrt(2) / 2 * XpYn, 0, - np.sqrt(2) / 2 * XpYn],
                                [0, 0, - Yn], [- np.sqrt(2) / 2 * XnYn, 0, - np.sqrt(2) / 2 * XnYn],
                                [- Xn, 0, 0], [- np.sqrt(2) / 2 * XnYp, 0, np.sqrt(2) / 2 * XnYp]
                                ]
        if normal == 'x':
            SlabShape_origin = [[0, Yp, 0], [0, np.sqrt(2) / 2 * XpYp, np.sqrt(2) / 2 * XpYp],
                                [0, 0, Xp], [0, - np.sqrt(2) / 2 * XpYn, np.sqrt(2) / 2 * XpYn],
                                [0, - Yn, 0], [0, - np.sqrt(2) / 2 * XnYn, - np.sqrt(2) / 2 * XnYn],
                                [0, 0, - Xn], [0, np.sqrt(2) / 2 * XnYp, - np.sqrt(2) / 2 * XnYp]
                                ]
        return np.dot(np.array(SlabShape_origin), np.array(R_matrix)) + np.tile(center, (8, 1))


class ProgressWin(QDialog, ProgressDialog):
    def __init__(self):
        super(ProgressWin, self).__init__()
        self.setupUi(self)


class AddSlabDialog(QDialog, SlabDialog):
    def __init__(self, path):
        super(AddSlabDialog, self).__init__()
        self.setupUi(self)
        self.project_dir = path
        self.label_project.setText('Current Project: ' + self.project_dir.split('/')[-1])
        self.pushBtn_SaveModel.setEnabled(False)
        self.pushBtn_View.setEnabled(False)
        self.normal = 'x'

        # for debugging
        self.lineEdit_SlabcenterX.setText('79500')
        self.lineEdit_SlabcenterY.setText('3560')
        self.lineEdit_SlabcenterZ.setText('-2000')
        self.lineEdit_SlabRalpha.setText('0')
        self.lineEdit_SlabRbeta.setText('0')
        self.lineEdit_SlabRtheta.setText('0')
        self.lineEdit_th.setText('200')
        self.lineEdit_val.setText('100')
        self.lineEdit_Yp.setText('200')
        self.lineEdit_Yn.setText('500')
        self.lineEdit_Xp.setText('500')
        self.lineEdit_Xn.setText('500')
        self.lineEdit_XnYn.setText('200')
        self.lineEdit_XpYp.setText('200')
        self.lineEdit_XpYn.setText('200')
        self.lineEdit_XnYp.setText('200')

        self.lineEdit_Yp.editingFinished.connect(self.setSlider_Yp)
        # self.lineEdit_Yp.returnPressed.connect(self.setSlider_Yp)
        self.horizontalSlider_Yp.valueChanged.connect(self.sliderValueChanged_Yp)

        self.lineEdit_Yn.editingFinished.connect(self.setSlider_Yn)
        self.horizontalSlider_Yn.valueChanged.connect(self.sliderValueChanged_Yn)

        self.lineEdit_Xp.editingFinished.connect(self.setSlider_Xp)
        self.horizontalSlider_Xp.valueChanged.connect(self.sliderValueChanged_Xp)

        self.lineEdit_Xn.editingFinished.connect(self.setSlider_Xn)
        self.horizontalSlider_Xn.valueChanged.connect(self.sliderValueChanged_Xn)

        self.lineEdit_XpYp.editingFinished.connect(self.setSlider_XpYp)
        self.horizontalSlider_XpYp.valueChanged.connect(self.sliderValueChanged_XpYp)

        self.lineEdit_XpYn.editingFinished.connect(self.setSlider_XpYn)
        self.horizontalSlider_XpYn.valueChanged.connect(self.sliderValueChanged_XpYn)

        self.lineEdit_XnYp.editingFinished.connect(self.setSlider_XnYp)
        self.horizontalSlider_XnYp.valueChanged.connect(self.sliderValueChanged_XnYp)

        self.lineEdit_XnYn.editingFinished.connect(self.setSlider_XnYn)
        self.horizontalSlider_XnYn.valueChanged.connect(self.sliderValueChanged_XnYn)

        self.pushBtn_Model_in.clicked.connect(self.load_model)
        self.pushBtn_Mesh.clicked.connect(self.load_mesh)
        self.pushBtn_View.clicked.connect(self.viewSlab)
        self.pushBtn_AddSlab.clicked.connect(self.add_slab)
        self.pushBtn_SaveModel.clicked.connect(self.save_model)

    @track_error
    def control_points(self):
        Yp = float(self.lineEdit_Yp.text())
        Yn = float(self.lineEdit_Yn.text())
        Xp = float(self.lineEdit_Xp.text())
        Xn = float(self.lineEdit_Xn.text())

        XpYp = float(self.lineEdit_XpYp.text())
        XpYn = float(self.lineEdit_XpYn.text())
        XnYp = float(self.lineEdit_XnYp.text())
        XnYn = float(self.lineEdit_XnYn.text())

        SlabcenterX = float(self.lineEdit_SlabcenterX.text())
        SlabcenterY = float(self.lineEdit_SlabcenterY.text())
        SlabcenterZ = float(self.lineEdit_SlabcenterZ.text())

        self.Slabalpha = float(self.lineEdit_SlabRalpha.text()) * np.pi / 180
        self.Slabbeta = float(self.lineEdit_SlabRbeta.text()) * np.pi / 180
        self.Slabtheta = float(self.lineEdit_SlabRtheta.text()) * np.pi / 180

        # clockwise
        if self.normal == 'z':
            SlabShape_origin = [[0, Yp, 0], [np.sqrt(2) / 2 * XpYp, np.sqrt(2) / 2 * XpYp, 0],
                                [Xp, 0, 0], [np.sqrt(2) / 2 * XpYn, - np.sqrt(2) / 2 * XpYn, 0],
                                [0, - Yn, 0], [- np.sqrt(2) / 2 * XnYn, - np.sqrt(2) / 2 * XnYn, 0],
                                [- Xn, 0, 0], [- np.sqrt(2) / 2 * XnYp, np.sqrt(2) / 2 * XnYp, 0]
                                ]
        if self.normal == 'y':
            SlabShape_origin = [[0, 0, Yp], [np.sqrt(2) / 2 * XpYp, 0, np.sqrt(2) / 2 * XpYp],
                                [Xp, 0, 0], [np.sqrt(2) / 2 * XpYn, 0, - np.sqrt(2) / 2 * XpYn],
                                [0, 0, - Yn], [- np.sqrt(2) / 2 * XnYn, 0, - np.sqrt(2) / 2 * XnYn],
                                [- Xn, 0, 0], [- np.sqrt(2) / 2 * XnYp, 0, np.sqrt(2) / 2 * XnYp]
                                ]
        if self.normal == 'x':
            SlabShape_origin = [[0, Yp, 0], [0, np.sqrt(2) / 2 * XpYp, np.sqrt(2) / 2 * XpYp],
                                [0, 0, Xp], [0, - np.sqrt(2) / 2 * XpYn, np.sqrt(2) / 2 * XpYn],
                                [0, - Yn, 0], [0, - np.sqrt(2) / 2 * XnYn, - np.sqrt(2) / 2 * XnYn],
                                [0, 0, - Xn], [0, np.sqrt(2) / 2 * XnYp, - np.sqrt(2) / 2 * XnYp]
                                ]

        self.Rotation()
        center = np.array([SlabcenterX, SlabcenterY, SlabcenterZ])
        self.sfLocInfo = np.dot(np.array(SlabShape_origin), np.array(self.R_matrix)) + np.tile(center, (8, 1))

    @track_error
    def Rotation(self):
        self.R_matrix = [[np.cos(self.Slabtheta) * np.cos(self.Slabbeta), \
                          - np.sin(self.Slabtheta) * np.cos(self.Slabalpha) + np.cos(self.Slabtheta) * np.sin(
                              self.Slabbeta) * np.sin(self.Slabalpha), \
                          np.sin(self.Slabtheta) * np.sin(self.Slabalpha) + np.cos(self.Slabtheta) * np.sin(
                              self.Slabbeta) * np.cos(self.Slabalpha)],
                         [np.sin(self.Slabtheta) * np.cos(self.Slabbeta), \
                          np.cos(self.Slabtheta) * np.cos(self.Slabalpha) + np.sin(self.Slabtheta) * np.sin(
                              self.Slabbeta) * np.sin(self.Slabalpha), \
                          - np.cos(self.Slabtheta) * np.sin(self.Slabalpha) + np.sin(self.Slabtheta) * np.sin(
                              self.Slabbeta) * np.cos(self.Slabalpha)],
                         [- np.sin(self.Slabbeta), \
                          np.cos(self.Slabbeta) * np.sin(self.Slabalpha), \
                          np.cos(self.Slabbeta) * np.cos(self.Slabalpha)]
                         ]

    @track_error
    def add_slab(self):
        # try:
        self.val = float(self.lineEdit_val.text())
        self.th = float(self.lineEdit_th.text())
        self.control_points()

        models = addModels(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
        self.model_out = models.addSlab(self.sfLocInfo, self.th, self.val, self.normal)

        if (self.nodeX is not None) and (self.model_out is not None):
            self.pushBtn_View.setEnabled(True)
            self.pushBtn_SaveModel.setEnabled(True)
            QMessageBox.information(self.pushBtn_AddSlab,
                                    "Add Slab",
                                    "Slab model added",
                                    QMessageBox.Yes)

        # except AttributeError:
        #     QMessageBox.warning(self.pushBtn_AddSlab,
        #                         "Error",
        #                         "Please load mesh and previous model!",
        #                         QMessageBox.Yes)
        #
        # except ValueError:
        #     QMessageBox.warning(self.pushBtn_AddSlab,
        #                         "Error",
        #                         "Please fill all necessary parameters!",
        #                         QMessageBox.Yes)

    @track_error
    def load_model(self):
        # open selector dialog
        self.model_select_win = SelectWin(os.path.join(self.project_dir, 'Background'), 'background')
        self.model_select_win.exec()
        if self.model_select_win.select_flag:
            self.label_model_in.setText('Previous Model: ' + self.model_select_win.selected_file)
            self.model_in = np.loadtxt(self.model_select_win.selected_path)

    @track_error
    def load_mesh(self):
        self.mesh_select_win = SelectWin(os.path.join(self.project_dir, 'Mesh'), 'mesh')
        self.mesh_select_win.exec()
        if self.mesh_select_win.select_flag:
            self.nodeX, self.nodeY, self.nodeZ = read_mesh_file(self.mesh_select_win.selected_path)
            self.label_mesh.setText('Mesh: ' + self.mesh_select_win.selected_file)

    @track_error
    def viewSlab(self):
        # except AttributeError
        try:
            self.model_out
        except AttributeError:
            QMessageBox.warning(self.pushBtn_View,
                                "Error",
                                "Please view the model after adding a slab!",
                                QMessageBox.Yes)
        else:
            self.ViewWin = pyvistaWin()
            self.ViewWin.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, self.model_out)
            self.ViewWin.show()
            # try expect KeyError

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
                QMessageBox.information(self, 'Saving Model',
                                        'Model saved.',
                                        QMessageBox.Yes)

    @track_error
    def setSlider_Yp(self):
        Yp_val = float(self.lineEdit_Yp.text())
        self.horizontalSlider_Yp.setMaximum(Yp_val * 1.5)
        self.horizontalSlider_Yp.setMinimum(Yp_val * 0.5)
        self.horizontalSlider_Yp.setValue(Yp_val)

    @track_error
    def setSlider_Yn(self):
        Yn_val = float(self.lineEdit_Yn.text())
        self.horizontalSlider_Yn.setMaximum(Yn_val * 1.5)
        self.horizontalSlider_Yn.setMinimum(Yn_val * 0.5)
        self.horizontalSlider_Yn.setValue(Yn_val)

    @track_error
    def setSlider_Xp(self):
        Xp_val = float(self.lineEdit_Xp.text())
        self.horizontalSlider_Xp.setMaximum(Xp_val * 1.5)
        self.horizontalSlider_Xp.setMinimum(Xp_val * 0.5)
        self.horizontalSlider_Xp.setValue(Xp_val)

    @track_error
    def setSlider_Xn(self):
        Xn_val = float(self.lineEdit_Xn.text())
        self.horizontalSlider_Xn.setMaximum(Xn_val * 1.5)
        self.horizontalSlider_Xn.setMinimum(Xn_val * 0.5)
        self.horizontalSlider_Xn.setValue(Xn_val)

    @track_error
    def setSlider_XpYp(self):
        XpYp_val = float(self.lineEdit_XpYp.text())
        self.horizontalSlider_XpYp.setMaximum(XpYp_val * 1.5)
        self.horizontalSlider_XpYp.setMinimum(XpYp_val * 0.5)
        self.horizontalSlider_XpYp.setValue(XpYp_val)

    @track_error
    def setSlider_XpYn(self):
        XpYn_val = float(self.lineEdit_XpYn.text())
        self.horizontalSlider_XpYn.setMaximum(XpYn_val * 1.5)
        self.horizontalSlider_XpYn.setMinimum(XpYn_val * 0.5)
        self.horizontalSlider_XpYn.setValue(XpYn_val)

    @track_error
    def setSlider_XnYp(self):
        XnYp_val = float(self.lineEdit_XnYp.text())
        self.horizontalSlider_XnYp.setMaximum(XnYp_val * 1.5)
        self.horizontalSlider_XnYp.setMinimum(XnYp_val * 0.5)
        self.horizontalSlider_XnYp.setValue(XnYp_val)

    @track_error
    def setSlider_XnYn(self):
        XnYn_val = float(self.lineEdit_XnYn.text())
        self.horizontalSlider_XnYn.setMaximum(XnYn_val * 1.5)
        self.horizontalSlider_XnYn.setMinimum(XnYn_val * 0.5)
        self.horizontalSlider_XnYn.setValue(XnYn_val)

    @track_error
    def sliderValueChanged_Yp(self):
        if self.lineEdit_Yp.text():
            value_show = float(self.horizontalSlider_Yp.value())
            self.lineEdit_Yp.setText(str(value_show))

    @track_error
    def sliderValueChanged_Yn(self):
        if self.lineEdit_Yn.text():
            value_show = float(self.horizontalSlider_Yn.value())
            self.lineEdit_Yn.setText(str(value_show))

    @track_error
    def sliderValueChanged_Xp(self):
        if self.lineEdit_Xp.text():
            value_show = float(self.horizontalSlider_Xp.value())
            self.lineEdit_Xp.setText(str(value_show))

    @track_error
    def sliderValueChanged_Xn(self):
        if self.lineEdit_Xn.text():
            value_show = float(self.horizontalSlider_Xn.value())
            self.lineEdit_Xn.setText(str(value_show))

    @track_error
    def sliderValueChanged_XpYp(self):
        if self.lineEdit_XpYp.text():
            value_show = float(self.horizontalSlider_XpYp.value())
            self.lineEdit_XpYp.setText(str(value_show))

    @track_error
    def sliderValueChanged_XpYn(self):
        if self.lineEdit_XpYn.text():
            value_show = float(self.horizontalSlider_XpYn.value())
            self.lineEdit_XpYn.setText(str(value_show))

    @track_error
    def sliderValueChanged_XnYp(self):
        if self.lineEdit_XnYp.text():
            value_show = float(self.horizontalSlider_XnYp.value())
            self.lineEdit_XnYp.setText(str(value_show))

    @track_error
    def sliderValueChanged_XnYn(self):
        if self.lineEdit_XnYn.text():
            value_show = float(self.horizontalSlider_XnYn.value())
            self.lineEdit_XnYn.setText(str(value_show))


class AddEllipsoidDialog(QDialog, EllipsoidDialog):
    def __init__(self,path):
        super(AddEllipsoidDialog, self).__init__()
        self.setupUi(self)
        self.project_dir = path
        self.label_project.setText('Current Project: ' + self.project_dir.split('/')[-1])
        self.pushBtn_SaveModel.setEnabled(False)
        self.pushBtn_View.setEnabled(False)

        # for debugging
        self.lineEdit_EllipsoidcenterX.setText('0')
        self.lineEdit_EllipsoidcenterY.setText('0')
        self.lineEdit_EllipsoidcenterZ.setText('3000')
        self.lineEdit_EllipsoidRalpha.setText('0')
        self.lineEdit_EllipsoidRbeta.setText('0')
        self.lineEdit_EllipsoidRtheta.setText('0')

        self.lineEdit_EllipsoidA.setText('1000')
        self.lineEdit_EllipsoidB.setText('500')
        self.lineEdit_EllipsoidC.setText('500')

        self.lineEdit_val.setText('20')

        self.pushBtn_Model_in.clicked.connect(self.load_model)
        self.pushBtn_Mesh.clicked.connect(self.load_mesh)
        self.pushBtn_View.clicked.connect(self.viewEllipsoid)
        self.pushBtn_AddEllipsoid.clicked.connect(self.add_ellipsoid)
        self.pushBtn_SaveModel.clicked.connect(self.save_model)

    @track_error
    def control_points(self):
        self.val_out=float(self.lineEdit_val.text())
        self.center=[float(self.lineEdit_EllipsoidcenterX.text()),float(self.lineEdit_EllipsoidcenterY.text()),float(self.lineEdit_EllipsoidcenterZ.text())]
        self.axis=[float(self.lineEdit_EllipsoidA.text()),float(self.lineEdit_EllipsoidB.text()),float(self.lineEdit_EllipsoidC.text())]
        self.angle=[float(self.lineEdit_EllipsoidRalpha.text()),float(self.lineEdit_EllipsoidRbeta.text()),float(self.lineEdit_EllipsoidRtheta.text())]

    @track_error
    def add_ellipsoid(self):
        try:
            self.control_points()
            self.val = float(self.lineEdit_val.text())

            models = addModels(self.nodeX, self.nodeY, self.nodeZ, self.model_in)
            self.model_out = models.addEllipsoid(self.center, self.angle, self.axis, self.val)

            if (self.nodeX is not None) and (self.model_out is not None):
                self.pushBtn_View.setEnabled(True)
                self.pushBtn_SaveModel.setEnabled(True)
                QMessageBox.information(self.pushBtn_AddEllipsoid,
                                        "Add Ellipsoid",
                                        "Ellipsoid model added",
                                        QMessageBox.Yes)
        except AttributeError:
            QMessageBox.warning(self.pushBtn_AddEllipsoid,
                                "Error",
                                "Please load mesh and previous model!",
                                QMessageBox.Yes)

        except ValueError:
            QMessageBox.warning(self.pushBtn_AddEllipsoid,
                                "Error",
                                "Please fill all necessary parameters!",
                                QMessageBox.Yes)

    @track_error
    def load_model(self):
        AddSlabDialog.load_model(self)

    @track_error
    def load_mesh(self):
        AddSlabDialog.load_mesh(self)

    @track_error
    def viewEllipsoid(self):
        AddSlabDialog.viewSlab(self)

    @track_error
    def save_model(self):
        AddSlabDialog.save_model(self)


class AddRandomEllipsoidDialog(QDialog, RandomEllipsoidDialog):
    def __init__(self, path):
        super(AddRandomEllipsoidDialog, self).__init__()
        self.setupUi(self)
        self.project_dir = path
        self.label_project.setText('Current Project: ' + self.project_dir.split('/')[-1])
        self.pushBtn_View.setEnabled(False)

        # for debugging
        self.lineEdit_count.setText('3')
        self.lineEdit_centerXmin.setText('0')
        self.lineEdit_centerYmin.setText('0')
        self.lineEdit_centerZmin.setText('-20')
        self.lineEdit_centerXmax.setText('5')
        self.lineEdit_centerYmax.setText('5')
        self.lineEdit_centerZmax.setText('-10')
        self.lineEdit_Ralphamin.setText('0')
        self.lineEdit_Rbetamin.setText('0')
        self.lineEdit_Rthetamin.setText('0')
        self.lineEdit_Ralphamax.setText('45')
        self.lineEdit_Rbetamax.setText('45')
        self.lineEdit_Rthetamax.setText('45')
        self.lineEdit_EllipsoidAmin.setText('2')
        self.lineEdit_EllipsoidBmin.setText('2')
        self.lineEdit_EllipsoidCmin.setText('2')
        self.lineEdit_EllipsoidAmax.setText('2')
        self.lineEdit_EllipsoidBmax.setText('2')
        self.lineEdit_EllipsoidCmax.setText('2')
        self.lineEdit_valmin.setText('2')
        self.checkBox_centerPoints.stateChanged.connect(self.random_filter)
        self.checkBox_rotation.stateChanged.connect(self.random_filter)
        self.checkBox_ABCaxis.stateChanged.connect(self.random_filter)
        self.checkBox_val.stateChanged.connect(self.random_filter)
        self.pushBtn_Model_in.clicked.connect(self.load_model)
        self.pushBtn_Mesh.clicked.connect(self.load_mesh)
        self.pushBtn_Gen.clicked.connect(self.randomGen)
        self.pushBtn_View.clicked.connect(self.viewEllipsoid)

    @track_error
    def random_filter(self):
        if self.checkBox_centerPoints.isChecked():
            self.label_centerXRange.setVisible(True)
            self.lineEdit_centerXmax.setVisible(True)
            self.label_centerYRange.setVisible(True)
            self.lineEdit_centerYmax.setVisible(True)
            self.label_centerZRange.setVisible(True)
            self.lineEdit_centerZmax.setVisible(True)
            self.label_center.setText('Center point: ')
        else:
            self.label_centerXRange.setVisible(False)
            self.lineEdit_centerXmax.setVisible(False)
            self.label_centerYRange.setVisible(False)
            self.lineEdit_centerYmax.setVisible(False)
            self.label_centerZRange.setVisible(False)
            self.lineEdit_centerZmax.setVisible(False)
            self.lineEdit_centerXmax.clear()
            self.lineEdit_centerYmax.clear()
            self.lineEdit_centerZmax.clear()
            self.label_center.setText('Center point fixed: ')
        if self.checkBox_rotation.isChecked():
            self.label_alphaRange.setVisible(True)
            self.lineEdit_Ralphamax.setVisible(True)
            self.label_betaRange.setVisible(True)
            self.lineEdit_Rbetamax.setVisible(True)
            self.label_thetaRange.setVisible(True)
            self.lineEdit_Rthetamax.setVisible(True)
            self.label_rotation.setText('Rotation (°):')
        else:
            self.label_alphaRange.setVisible(False)
            self.lineEdit_Ralphamax.setVisible(False)
            self.label_betaRange.setVisible(False)
            self.lineEdit_Rbetamax.setVisible(False)
            self.label_thetaRange.setVisible(False)
            self.lineEdit_Rthetamax.setVisible(False)
            self.lineEdit_Ralphamax.clear()
            self.lineEdit_Rbetamax.clear()
            self.lineEdit_Rthetamax.clear()
            self.label_rotation.setText('Rotation (°) fixed:')
        if self.checkBox_ABCaxis.isChecked():
            self.label_aRange.setVisible(True)
            self.lineEdit_EllipsoidAmax.setVisible(True)
            self.label_bRange.setVisible(True)
            self.lineEdit_EllipsoidBmax.setVisible(True)
            self.label_cRange.setVisible(True)
            self.lineEdit_EllipsoidCmax.setVisible(True)
            self.label_EllipsoidAxis.setText('Axis length: ')
        else:
            self.label_aRange.setVisible(False)
            self.lineEdit_EllipsoidAmax.setVisible(False)
            self.label_bRange.setVisible(False)
            self.lineEdit_EllipsoidBmax.setVisible(False)
            self.label_cRange.setVisible(False)
            self.lineEdit_EllipsoidCmax.setVisible(False)
            self.lineEdit_EllipsoidAmax.clear()
            self.lineEdit_EllipsoidBmax.clear()
            self.lineEdit_EllipsoidCmax.clear()
            self.label_EllipsoidAxis.setText('Axis length fixed: ')
        if self.checkBox_val.isChecked():
            self.label_valRange.setVisible(True)
            self.lineEdit_valmax.setVisible(True)
            self.label_val.setText('Value: ')
        else:
            self.label_valRange.setVisible(False)
            self.lineEdit_valmax.setVisible(False)
            self.lineEdit_valmax.clear()
            self.label_val.setText('Value fixed: ')
        if self.checkBox_centerPoints.checkState() == 0 and \
           self.checkBox_rotation.checkState() == 0 and \
           self.checkBox_val.checkState() == 0 and \
           self.checkBox_ABCaxis.checkState() == 0:
            QMessageBox.warning(self,
                                "Warning",
                                "Cannot generate more than 2 different slab models! \
                                 'Number' will be set to 1",
                                QMessageBox.Yes)
            self.lineEdit_count.setText('1')

    @track_error
    def randomGen(self):
        try:
            mincenterX = float(self.lineEdit_centerXmin.text())
            mincenterY = float(self.lineEdit_centerYmin.text())
            mincenterZ = float(self.lineEdit_centerZmin.text())
            minRalpha = float(self.lineEdit_Ralphamin.text()) * np.pi / 180
            minRbeta = float(self.lineEdit_Rbetamin.text()) * np.pi / 180
            minRtheta = float(self.lineEdit_Rthetamin.text()) * np.pi / 180
            minAaxis = float(self.lineEdit_EllipsoidAmin.text())
            minBaxis = float(self.lineEdit_EllipsoidBmin.text())
            minCaxis = float(self.lineEdit_EllipsoidCmin.text())
            minVal = float(self.lineEdit_valmin.text())
            if self.checkBox_centerPoints.checkState() == 0:
                self.lineEdit_centerXmax.setText(str(mincenterX))
                self.lineEdit_centerYmax.setText(str(mincenterY))
                self.lineEdit_centerZmax.setText(str(mincenterZ))
            if self.checkBox_rotation.checkState() == 0:
                self.lineEdit_Ralphamax.setText(str(minRalpha))
                self.lineEdit_Rbetamax.setText(str(minRbeta))
                self.lineEdit_Rthetamax.setText(str(minRtheta))
            if self.checkBox_ABCaxis.checkState() == 0:
                self.lineEdit_EllipsoidAmax.setText(str(minAaxis))
                self.lineEdit_EllipsoidBmax.setText(str(minBaxis))
                self.lineEdit_EllipsoidCmax.setText(str(minCaxis))
            if self.checkBox_val.checkState() == 0:
                self.lineEdit_valmax.setText(str(minVal))
            self.model_count = int(self.lineEdit_count.text())
            maxcenterX = float(self.lineEdit_centerXmax.text())
            maxcenterY = float(self.lineEdit_centerYmax.text())
            maxcenterZ = float(self.lineEdit_centerZmax.text())
            centerX_Set = np.random.uniform(mincenterX, maxcenterX, self.model_count)
            centerY_Set = np.random.uniform(mincenterY, maxcenterY, self.model_count)
            centerZ_Set = np.random.uniform(mincenterZ, maxcenterZ, self.model_count)
            maxRalpha = float(self.lineEdit_Ralphamax.text()) * np.pi / 180
            maxRbeta = float(self.lineEdit_Rbetamax.text()) * np.pi / 180
            maxRtheta = float(self.lineEdit_Rthetamax.text()) * np.pi / 180
            Ralpha_Set = np.random.uniform(minRalpha, maxRalpha, self.model_count)
            Rbeta_Set = np.random.uniform(minRbeta, maxRbeta, self.model_count)
            Rtheta_Set = np.random.uniform(minRtheta, maxRtheta, self.model_count)
            maxAaxis = float(self.lineEdit_EllipsoidAmax.text())
            maxBaxis = float(self.lineEdit_EllipsoidBmax.text())
            maxCaxis = float(self.lineEdit_EllipsoidCmax.text())
            Axis_Set = np.random.uniform(minAaxis, maxAaxis, self.model_count)
            Bxis_Set = np.random.uniform(minBaxis, maxBaxis, self.model_count)
            Cxis_Set = np.random.uniform(minCaxis, maxCaxis, self.model_count)
            maxVal = float(self.lineEdit_valmax.text())
            ElliposoidVal_Set = np.random.uniform(minVal, maxVal, self.model_count)

            self.random_gen_worker = GenerationWorker()
            self.thread_ellipsoid_random_gen = QtCore.QThread()
            self.random_gen_worker.moveToThread(self.thread_ellipsoid_random_gen)
            self.random_gen_worker.start_random_gen.connect(lambda: self.pushBtn_Gen.setEnabled(False))
            self.random_gen_worker.finish_random_gen.connect(lambda: self.pushBtn_View.setEnabled(True))
            self.random_gen_worker.finish_random_gen.connect(lambda: self.pushBtn_Gen.setEnabled(True))
            self.random_gen_worker.finish_random_gen.connect(self.gen_finished)
            self.random_gen_worker.finish_random_gen.connect(self.thread_ellipsoid_random_gen.quit)
            self.random_gen_worker.on_each_loop_end_signal.connect(self.update_gen_progress)
            self.random_gen_worker.no_dir_signal.connect(self.no_dir)
            QtCore.QTimer.singleShot(0, partial(self.random_gen_worker.ellipsoid_random_gen,
                                                self.project_dir, self.model_count,
                                                self.nodeX, self.nodeY, self.nodeZ, self.model_in,
                                                centerX_Set, centerY_Set, centerZ_Set,
                                                Ralpha_Set, Rbeta_Set, Rtheta_Set,
                                                Axis_Set, Bxis_Set, Cxis_Set,
                                                ElliposoidVal_Set
                                                ))
            self.thread_ellipsoid_random_gen.start()
            self.show_gen_progress()

        except AttributeError:
            QMessageBox.warning(self.pushBtn_Gen,
                                "Error",
                                "Please load mesh and previous model!",
                                QMessageBox.Yes)
        except ValueError:
            QMessageBox.warning(self.pushBtn_Gen,
                                "Error",
                                "Please fill all necessary parameters!",
                                QMessageBox.Yes)

    @track_error
    def show_gen_progress(self):
        self.gen_progress = ProgressWin()
        self.gen_progress.exec()

    @track_error_args
    def update_gen_progress(self, i):
        self.gen_progress.progressBar.setValue(int((i + 1) / int(self.model_count) * 100))

    @track_error
    def gen_finished(self):
        self.gen_progress.close()
        QMessageBox.information(self.pushBtn_Gen,
                                "Ellipsoids Generation",
                                "Ellipsoid models generated",
                                QMessageBox.Yes)

    @track_error
    def no_dir(self):
        QMessageBox.critical(self.pushBtn_Gen, 'Error',
                             'Please use right path!',
                             QMessageBox.Yes)

    @track_error
    def load_model(self):
        # open selector dialog
        AddEllipsoidDialog.load_model(self)

    @track_error
    def load_mesh(self):
        AddEllipsoidDialog.load_mesh(self)

    @track_error
    def viewEllipsoid(self):
        random_ellipsoid_view_win = SelectWin(os.path.join(self.project_dir, 'Model'), 'model')
        random_ellipsoid_view_win.exec()
        if random_ellipsoid_view_win.select_flag:
            model_in = np.loadtxt(random_ellipsoid_view_win.selected_path)
            self.showWin = pyvistaWin()
            self.showWin.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, model_in)
            self.showWin.show()


class AddRandomSlabDialog(QDialog, RandomSlabDialog):
    def __init__(self, path):
        super(AddRandomSlabDialog, self).__init__()
        self.setupUi(self)
        self.project_dir = path
        self.label_project.setText('Current Project: ' + self.project_dir.split('/')[-1])
        self.pushBtn_View.setEnabled(False)
        self.normal = 'x'

        # for debugging
        self.lineEdit_count.setText('3')
        self.lineEdit_SlabcenterXmin.setText('-400')
        self.lineEdit_SlabcenterYmin.setText('-400')
        self.lineEdit_SlabcenterZmin.setText('-400')
        self.lineEdit_SlabcenterXmax.setText('400')
        self.lineEdit_SlabcenterYmax.setText('400')
        self.lineEdit_SlabcenterZmax.setText('400')
        self.lineEdit_SlabRalphamin.setText('0')
        self.lineEdit_SlabRbetamin.setText('0')
        self.lineEdit_SlabRthetamin.setText('0')
        self.lineEdit_SlabRalphamax.setText('45')
        self.lineEdit_SlabRbetamax.setText('45')
        self.lineEdit_SlabRthetamax.setText('45')
        self.lineEdit_directionmin.setText('100')
        self.lineEdit_directionmax.setText('300')
        self.lineEdit_thmin.setText('100')
        self.lineEdit_thmax.setText('300')
        self.lineEdit_valmin.setText('3')
        self.lineEdit_valmax.setText('6')
        self.checkBox_rotation.stateChanged.connect(self.random_filter)
        self.checkBox_centerPoints.stateChanged.connect(self.random_filter)
        self.checkBox_th.stateChanged.connect(self.random_filter)
        self.checkBox_val.stateChanged.connect(self.random_filter)
        self.checkBox_directionL.stateChanged.connect(self.random_filter)
        self.pushBtn_Model_in.clicked.connect(self.load_model)
        self.pushBtn_Mesh.clicked.connect(self.load_mesh)
        self.pushBtn_View.clicked.connect(self.viewSlab)
        self.pushBtn_Gen.clicked.connect(self.randomGen)

    @track_error
    def random_filter(self):
        if self.checkBox_rotation.isChecked():
            self.label_alphaRange.setVisible(True)
            self.lineEdit_SlabRalphamax.setVisible(True)
            self.label_betaRange.setVisible(True)
            self.lineEdit_SlabRbetamax.setVisible(True)
            self.label_thetaRange.setVisible(True)
            self.lineEdit_SlabRthetamax.setVisible(True)
            self.label_rotation.setText('Rotation (°):')
        else:
            self.label_alphaRange.setVisible(False)
            self.lineEdit_SlabRalphamax.setVisible(False)
            self.label_betaRange.setVisible(False)
            self.lineEdit_SlabRbetamax.setVisible(False)
            self.label_thetaRange.setVisible(False)
            self.lineEdit_SlabRthetamax.setVisible(False)
            self.lineEdit_SlabRalphamax.clear()
            self.lineEdit_SlabRbetamax.clear()
            self.lineEdit_SlabRthetamax.clear()
            self.label_rotation.setText('Rotation (°) fixed:')
        if self.checkBox_centerPoints.isChecked():
            self.label_centerXRange.setVisible(True)
            self.lineEdit_SlabcenterXmax.setVisible(True)
            self.label_centerYRange.setVisible(True)
            self.lineEdit_SlabcenterYmax.setVisible(True)
            self.label_centerZRange.setVisible(True)
            self.lineEdit_SlabcenterZmax.setVisible(True)
            self.label_center.setText('Center point: ')
        else:
            self.label_centerXRange.setVisible(False)
            self.lineEdit_SlabcenterXmax.setVisible(False)
            self.label_centerYRange.setVisible(False)
            self.lineEdit_SlabcenterYmax.setVisible(False)
            self.label_centerZRange.setVisible(False)
            self.lineEdit_SlabcenterZmax.setVisible(False)
            self.lineEdit_SlabcenterXmax.clear()
            self.lineEdit_SlabcenterYmax.clear()
            self.lineEdit_SlabcenterZmax.clear()
            self.label_center.setText('Center point fixed: ')
        if self.checkBox_th.isChecked():
            self.label_thRange.setVisible(True)
            self.lineEdit_thmax.setVisible(True)
            self.label_th.setText('Thickness: ')
        else:
            self.label_thRange.setVisible(False)
            self.lineEdit_thmax.setVisible(False)
            self.lineEdit_thmax.clear()
            self.label_th.setText('Thickness fixed: ')
        if self.checkBox_val.isChecked():
            self.label_valRange.setVisible(True)
            self.lineEdit_valmax.setVisible(True)
            self.label_val.setText('Value: ')
        else:
            self.label_valRange.setVisible(False)
            self.lineEdit_valmax.setVisible(False)
            self.lineEdit_valmax.clear()
            self.label_val.setText('Value fixed: ')
        if self.checkBox_directionL.isChecked():
            self.label_directionRange.setVisible(True)
            self.lineEdit_directionmax.setVisible(True)
            self.label_direction.setText('Directional 8 axes lengths: ')
        else:
            self.label_direction.setText('Directional 8 axes lengths fixed: ')
        if self.checkBox_rotation.checkState() == 0 and \
           self.checkBox_centerPoints.checkState() == 0 and \
           self.checkBox_th.checkState() == 0 and \
           self.checkBox_val.checkState() == 0 and \
           self.checkBox_directionL.checkState() == 0:
            QMessageBox.warning(self,
                                "Warning",
                                "Cannot generate more than 2 different slab models! \
                                 'Number' will be set to 1",
                                QMessageBox.Yes)
            self.lineEdit_count.setText('1')

    @track_error
    def randomGen(self):
        try:
            minSlabcenterX = float(self.lineEdit_SlabcenterXmin.text())
            minSlabcenterY = float(self.lineEdit_SlabcenterYmin.text())
            minSlabcenterZ = float(self.lineEdit_SlabcenterZmin.text())
            minSlabRalpha = float(self.lineEdit_SlabRalphamin.text())
            minSlabRbeta = float(self.lineEdit_SlabRbetamin.text())
            minSlabRtheta = float(self.lineEdit_SlabRthetamin.text())
            minLength = float(self.lineEdit_directionmin.text())
            minTh = float(self.lineEdit_thmin.text())
            minVal = float(self.lineEdit_valmin.text())
            if self.checkBox_centerPoints.checkState() == 0:
                self.lineEdit_SlabcenterXmax.setText(str(minSlabcenterX))
                self.lineEdit_SlabcenterYmax.setText(str(minSlabcenterY))
                self.lineEdit_SlabcenterZmax.setText(str(minSlabcenterZ))
            if self.checkBox_rotation.checkState() == 0:
                self.lineEdit_SlabRalphamax.setText(str(minSlabRalpha))
                self.lineEdit_SlabRbetamax.setText(str(minSlabRbeta))
                self.lineEdit_SlabRthetamax.setText(str(minSlabRtheta))
            if self.checkBox_th.checkState() == 0:
                self.lineEdit_thmax.setText(str(minTh))
            if self.checkBox_val.checkState() == 0:
                self.lineEdit_valmax.setText(str(minVal))
            self.model_count = int(self.lineEdit_count.text())
            maxSlabcenterX = float(self.lineEdit_SlabcenterXmax.text())
            maxSlabcenterY = float(self.lineEdit_SlabcenterYmax.text())
            maxSlabcenterZ = float(self.lineEdit_SlabcenterZmax.text())
            SlabcenterX_Set = np.random.uniform(minSlabcenterX, maxSlabcenterX, self.model_count)
            SlabcenterY_Set = np.random.uniform(minSlabcenterY, maxSlabcenterY, self.model_count)
            SlabcenterZ_Set = np.random.uniform(minSlabcenterZ, maxSlabcenterZ, self.model_count)
            maxSlabRalpha = float(self.lineEdit_SlabRalphamax.text())
            maxSlabRbeta = float(self.lineEdit_SlabRbetamax.text())
            maxSlabRtheta = float(self.lineEdit_SlabRthetamax.text())
            SlabRalpha_Set = np.random.uniform(minSlabRalpha, maxSlabRalpha, self.model_count)
            SlabRbeta_Set = np.random.uniform(minSlabRbeta, maxSlabRbeta, self.model_count)
            SlabRtheta_Set = np.random.uniform(minSlabRtheta, maxSlabRtheta, self.model_count)
            maxLength = float(self.lineEdit_directionmax.text())
            if self.checkBox_directionL.checkState() == 0:
                ControlLengths = np.random.uniform(minLength, maxLength, 8)
                ControlLength_Set = np.tile(np.array([ControlLengths]).transpose(),
                                            (1, self.model_count))
            else:
                ControlLength_Set = np.random.uniform(minLength, maxLength, (8, self.model_count))
            maxTh = float(self.lineEdit_thmax.text())
            SlabTh_Set = np.random.uniform(minTh, maxTh, self.model_count)
            maxVal = float(self.lineEdit_valmax.text())
            SlabVal_Set = np.random.uniform(minVal, maxVal, self.model_count)

            self.random_gen_worker = GenerationWorker()
            self.thread_slab_random_gen = QtCore.QThread()
            self.random_gen_worker.moveToThread(self.thread_slab_random_gen)
            self.random_gen_worker.start_random_gen.connect(lambda: self.pushBtn_Gen.setEnabled(False))
            self.random_gen_worker.finish_random_gen.connect(lambda: self.pushBtn_View.setEnabled(True))
            self.random_gen_worker.finish_random_gen.connect(lambda: self.pushBtn_Gen.setEnabled(True))
            self.random_gen_worker.finish_random_gen.connect(self.gen_finished)
            self.random_gen_worker.finish_random_gen.connect(self.thread_slab_random_gen.quit)
            self.random_gen_worker.on_each_loop_end_signal.connect(self.update_gen_progress)
            self.random_gen_worker.no_dir_signal.connect(self.no_dir)
            QtCore.QTimer.singleShot(0, partial(self.random_gen_worker.slab_random_gen,
                                                self.project_dir, self.model_count, self.normal,
                                                self.nodeX, self.nodeY, self.nodeZ, self.model_in,
                                                ControlLength_Set,
                                                SlabcenterX_Set, SlabcenterY_Set, SlabcenterZ_Set,
                                                SlabRalpha_Set, SlabRbeta_Set, SlabRtheta_Set,
                                                SlabVal_Set, SlabTh_Set
                                                ))
            self.thread_slab_random_gen.start()
            self.show_gen_progress()

        except AttributeError:
            QMessageBox.warning(self.pushBtn_Gen,
                                "Error",
                                "Please load mesh and previous model!",
                                QMessageBox.Yes)
        except ValueError:
            QMessageBox.warning(self.pushBtn_Gen,
                                "Error",
                                "Please fill all necessary parameters!",
                                QMessageBox.Yes)

    @track_error
    def show_gen_progress(self):
        self.gen_progress = ProgressWin()
        self.gen_progress.exec()
        # self.gen_progress.open()
        # self.gen_progress.finished.connect(self.gen_finished)

    @track_error_args
    def update_gen_progress(self, i):
        self.gen_progress.progressBar.setValue(int((i + 1) / int(self.model_count) * 100))

    @track_error
    def gen_finished(self):
        self.gen_progress.close()
        QMessageBox.information(self.pushBtn_Gen,
                                "Slabs Generation",
                                "Slab models generated",
                                QMessageBox.Yes)

    @track_error
    def no_dir(self):
        QMessageBox.critical(self.pushBtn_Gen, 'Error',
                             'Please use right path!',
                             QMessageBox.Yes)

    @track_error
    def load_model(self):
        # open selector dialog
        AddSlabDialog.load_model(self)

    @track_error
    def load_mesh(self):
        AddSlabDialog.load_mesh(self)

    @track_error
    def viewSlab(self):
        random_slab_view_win = SelectWin(os.path.join(self.project_dir, 'Model'), 'model')
        random_slab_view_win.exec()
        if random_slab_view_win.select_flag:
            model_in = np.loadtxt(random_slab_view_win.selected_path)
            self.showWin = pyvistaWin()
            self.showWin.view_model_ubc(self.nodeX, self.nodeY, self.nodeZ, model_in)
            self.showWin.show()
