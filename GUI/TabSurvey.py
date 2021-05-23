from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie

from UI_init.Ui_tabSurvey import Ui_tab_survey
from UI_init.Ui_loadingWin import Ui_LoadingWin

from GUI.DoubleSelectWin import DoubleSelectWin
from GUI.FilenameSetting import FileNameSettingWin
from GUI.XYZTable import XYZTable

from functions.rcvsetting import rcvsetting

import os
import numpy as np
# import shutil
from functools import partial
from scipy.interpolate import griddata
from pyvistaqt import QtInteractor
import pyvista as pv


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
            QMessageBox.Critical(self, 'Test Error', str(e), QMessageBox.Yes)
    return wrapper


def finished_reminder(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Finished', 'Task finished.', QMessageBox.Yes)
    return wrapper


def finished_reminder_new(win_title, info):
    def deco_func(func):
        def wrapper(self):
            func(self)
            QMessageBox.information(self, win_title, info, QMessageBox.Yes)
        return wrapper
    return deco_func()


def not_finished_yet(func):
    def wrapper(self):
        func(self)
        QMessageBox.information(self, 'Information', 'NOT FINISHED YET...', QMessageBox.Yes)
    return wrapper


class LoadingWin(QDialog, Ui_LoadingWin):
    def __init__(self):
        super(LoadingWin, self).__init__()
        self.setupUi(self)

        self.movie = QMovie('ProgressBar.gif')
        self.label.setMovie(self.movie)
        self.setWindowTitle('Topo data Loading')
        self.setFixedSize(300, 150)

        self.start_animation()

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
        self.close()


class TopoWorker(QtCore.QObject):
    start_job = QtCore.pyqtSignal()
    finish_job = QtCore.pyqtSignal()

    def __init__(self):
        super(TopoWorker, self).__init__()

        self.loadingWin = LoadingWin()
        self.loadingWin.show()

    @track_error_args
    def import_topo(self, topo_dir):
        self.start_job.emit()
        self.topo_data = np.loadtxt(topo_dir, delimiter=',')
        # print('Loading topo finished!')
        self.loadingWin.close()
        self.finish_job.emit()


class AddTabSurvey(QTabWidget, Ui_tab_survey):
    def __init__(self, path):
        super(AddTabSurvey, self).__init__()
        self.setupUi(self)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 7)
        # self.splitter.setSizes([self.splitter.size().width() * 0.3,
        #                         self.splitter.size().width() * 0.7])
        self.project_dir = path

        # topo
        self.topo_data = None
        self.topo_init()
        self.checkBox_topo.stateChanged.connect(self.use_topo)
        self.pushButton_topoBrowser.clicked.connect(self.load_topo_path)

        # src
        self.table_src = XYZTable(nc=3, Hheaders=['X', 'Y', 'Z'])
        self.checkBox_srcint.setChecked(False)
        self.activate_src_int_setting()
        self.tableWidget_src = self.table_src.tableWidget
        self.verticalLayout_src_table.addWidget(self.tableWidget_src)
        self.table_src.zero_margin()

        self.lineEdit_srcnum.editingFinished.connect(self.src_table_update)
        self.checkBox_srcint.stateChanged.connect(self.activate_src_int_setting)
        self.pushButton_clear_src.clicked.connect(self.src_table_init)
        self.pushButton_import_src.clicked.connect(self.import_src)
        self.pushButton_save_src.clicked.connect(self.save_src_setting)

        # rcv
        self.table_rcv = XYZTable(nc=6, Hheaders=['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2'])
        self.tableWidget_rcv = self.table_rcv.tableWidget
        self.verticalLayout_rcv_table.addWidget(self.tableWidget_rcv)
        self.table_rcv.zero_margin()

        self.rcv_path_x = None
        self.rcv_path_y = None
        self.rcv_import_flag = False

        self.pushButton_clear_rcv.clicked.connect(self.rcv_table_init)
        self.pushButton_import_rcv.clicked.connect(self.import_rcv)
        self.pushButton_save_rcv.clicked.connect(self.save_rcv_setting)

        # View
        self.plotter = QtInteractor(self.groupBox_View)
        self.verticalLayout_view.addWidget(self.plotter.interactor)
        self.pushButton_viewSurvey.clicked.connect(self.view_survey)
        self.pushButton_viewWellpaths.clicked.connect(self.view_added_wellpaths)
        self.pushButton_clearView.clicked.connect(self.clear_view)

    @track_error
    def topo_init(self):
        self.checkBox_topo.setChecked(False)
        self.lineEdit_topo.setEnabled(False)
        self.pushButton_topoBrowser.setEnabled(False)

    @track_error
    def use_topo(self):
        if self.checkBox_topo.isChecked():
            self.lineEdit_topo.setEnabled(True)
            self.pushButton_topoBrowser.setEnabled(True)
        else:
            self.lineEdit_topo.setEnabled(False)
            self.pushButton_topoBrowser.setEnabled(False)
            self.lineEdit_topo.clear()
            self.topo_init()

    @track_error
    def load_topo_path(self):
        self.topo_dir, tmp = QFileDialog.getOpenFileName(self,
                                                         "Choose a topography data file",
                                                         "*")
        if self.topo_dir:
            self.lineEdit_topo.setText(self.topo_dir)

            self.job_worker = TopoWorker()
            self.thread_loading_topo_file = QtCore.QThread()
            self.job_worker.moveToThread(self.thread_loading_topo_file)
            self.job_worker.finish_job.connect(self.loading_finished)
            self.job_worker.finish_job.connect(self.thread_loading_topo_file.quit)
            QtCore.QTimer.singleShot(0, partial(self.job_worker.import_topo, self.topo_dir))
            self.thread_loading_topo_file.start()

    @track_error_args
    def update_elevation_src(self, src_path):
        src_path_elevation = self.update_elevation(topo_data=self.topo_data,
                                                   points=src_path)
        self.table_src.points_to_table_column(np.round(src_path_elevation, 6), 2)

    @track_error_args
    def update_elevation_rcv(self, rcv_path):
        # show
        rcv_path_elevation_1 = self.update_elevation(topo_data=self.topo_data,
                                                     points=rcv_path[:, :3])
        rcv_path_elevation_2 = self.update_elevation(topo_data=self.topo_data,
                                                     points=rcv_path[:, 3:])
        self.table_rcv.points_to_table_column(np.round(rcv_path_elevation_1, 6), 2)
        self.table_rcv.points_to_table_column(np.round(rcv_path_elevation_2, 6), 5)

    @track_error_args
    def update_elevation(self, topo_data, points):
        z = griddata(topo_data[:, :2], topo_data[:, 2], points[:, (0, 1)])
        return z

    def get_src_loc(self):
        src_ctrl_points = np.empty((self.tableWidget_src.rowCount(), 3))
        for i in range(self.tableWidget_src.rowCount()):
            src_ctrl_points[i, 0] = float(self.tableWidget_src.item(i, 0).text())
            src_ctrl_points[i, 1] = float(self.tableWidget_src.item(i, 1).text())
            src_ctrl_points[i, 2] = float(self.tableWidget_src.item(i, 2).text())

        if self.lineEdit_srcint.isEnabled():
            try:
                d = float(self.lineEdit_srcint.text())
                self.src_discrete_points = self.discrete_src_path(src_ctrl_points=src_ctrl_points,
                                                                  d=d)
                return True
            except ValueError:
                QMessageBox.critical(self.pushButton_save_src,
                                     'Error', 'Please set correct interval (float)!',
                                     QMessageBox.Yes)
                return False
        else:
            self.src_discrete_points = src_ctrl_points
            return True

    def discrete_src_path(self, src_ctrl_points, d):
        src_discrete_points = []
        for i in range(src_ctrl_points.shape[0] - 1):
            dx = (src_ctrl_points[i + 1, 0] - src_ctrl_points[i, 0])
            dy = (src_ctrl_points[i + 1, 1] - src_ctrl_points[i, 1])
            dz = (src_ctrl_points[i + 1, 2] - src_ctrl_points[i, 2])
            length = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
            n = np.ceil(length / d)
            for j in range(int(n)):
                src_discrete_points.append([src_ctrl_points[i][0] + j * d * (dx / length),
                                            src_ctrl_points[i][1] + j * d * (dy / length),
                                            src_ctrl_points[i][2] + j * d * (dz / length)])
            src_discrete_points.append([src_ctrl_points[i + 1][0] - (length % d) * (dx / length),
                                        src_ctrl_points[i + 1][1] - (length % d) * (dy / length),
                                        src_ctrl_points[i + 1][2] - (length % d) * (dz / length)])
        return np.array(src_discrete_points)

    @track_error
    def save_src_setting(self):
        flag = self.get_src_loc()
        if flag:
            save_win = FileNameSettingWin()
            project_name = self.project_dir.split('/')[-1]
            save_win.label_path.setText('%s/Survey/Source/' % project_name)
            save_win.label_filename.setText('Source config filename: ')
            save_win.exec()

            if save_win.create_flag:
                src_filename = save_win.lineEdit_filename.text() + '.txt'
                src_config_path = os.path.join(self.project_dir, *['Survey', 'Source', src_filename])

                np.savetxt(src_config_path,
                           self.src_discrete_points,
                           fmt='%.6f',
                           delimiter=',')
                QMessageBox.information(self, 'Saving source configuration',
                                        'Current source configuration saved.',
                                        QMessageBox.Yes)

    @track_error
    def import_src(self):
        source_dir, tmp = QFileDialog.getOpenFileName(self,
                                                      "Choose source file",
                                                      "*")
        if source_dir:
            src_points = np.loadtxt(source_dir, delimiter=',')
            self.label_srcfile.setText(source_dir.split('/')[-1])
            self.lineEdit_srcint.clear()
            self.checkBox_srcint.setChecked(False)
            self.lineEdit_srcnum.setText(str(src_points.shape[0]))
            if self.topo_data is None:
                self.table_src.points_to_table(src_points)
            else:
                reply = QMessageBox.question(self.pushButton_import_src,
                                             'Use topo data?',
                                             'Do you want to interpolate path points from the loaded elevation data?',
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.table_src.points_to_table(src_points)
                    self.update_elevation_src(src_points)
                else:
                    self.table_src.points_to_table(src_points)

            QMessageBox.information(self.pushButton_import_src,
                                    'Import data',
                                    'Import source path data successfully.',
                                    QMessageBox.Yes)
            # # copy file
            # shutil.copy(source_dir, os.path.join(self.project_dir, *['Survey', 'Source']))

    @track_error
    def src_table_update(self):
        self.table_src.table_init(int(self.lineEdit_srcnum.text()))

    def src_table_init(self):
        self.table_src.table_init(0)
        self.label_srcfile.clear()
        self.checkBox_srcint.setChecked(False)
        self.lineEdit_srcint.clear()
        self.lineEdit_srcnum.clear()
        self.pushButton_save_src.setEnabled(True)

    @track_error
    def get_rcv_loc(self):
        if self.lineEdit_rcvXmin.isEnabled():
            x_start = float(self.lineEdit_rcvXmin.text())
            x_end = float(self.lineEdit_rcvXmax.text())
            x_interval = float(self.lineEdit_rcvXint.text())
            y_start = float(self.lineEdit_rcvYmin.text())
            y_end = float(self.lineEdit_rcvYmax.text())
            y_interval = float(self.lineEdit_rcvYint.text())

            self.rcv_path_x, self.rcv_path_y = rcvsetting(xspacestart=x_start,
                                                          xspaceend=x_end,
                                                          xinterval=x_interval,
                                                          yspacestart=y_start,
                                                          yspaceend=y_end,
                                                          yinterval=y_interval)
            self.rcv_import_flag = False
        else:
            self.rcv_path = self.table_rcv.table_to_points()
            self.rcv_import_flag = True

    @track_error
    def save_rcv_setting(self):
        self.get_rcv_loc()
        if self.rcv_import_flag:
            save_win = FileNameSettingWin()
            project_name = self.project_dir.split('/')[-1]
            save_win.label_path.setText('%s/Survey/Source/' % project_name)
            save_win.label_filename.setText('Source config filename: ')
            save_win.exec()

            if save_win.create_flag:
                # save rcv_path
                src_filename = save_win.lineEdit_filename.text() + '.txt'
                rcv_config_path = os.path.join(self.project_dir, *['Survey', 'Receiver', src_filename])
                np.savetxt(rcv_config_path,
                           self.rcv_path,
                           delimiter=',')
                QMessageBox.information(self, 'Saving receiver configuration',
                                        'Current receiver configuration saved.',
                                        QMessageBox.Yes)
        else:
            if (self.rcv_path_x is None) and (self.rcv_path_y is None):
                QMessageBox.warning(self.pushButton_save_rcv, 'Error',
                                    'Nonstandard receiver setting.',
                                    QMessageBox.Yes)
            else:
                save_win = FileNameSettingWin()
                project_name = self.project_dir.split('/')[-1]
                save_win.label_path.setText('%s/Survey/Source/' % project_name)
                save_win.label_filename.setText('Source config filename: ')
                save_win.exec()

                if save_win.create_flag:
                    # save rcv_path_x
                    src_filename_x = save_win.lineEdit_filename.text() + '_x.txt'
                    rcv_config_path_x = os.path.join(self.project_dir, *['Survey', 'Receiver', src_filename_x])
                    np.savetxt(rcv_config_path_x,
                               self.rcv_path_x,
                               delimiter=',')
                    # save rcv_path_y
                    src_filename_y = save_win.lineEdit_filename.text() + '_y.txt'
                    rcv_config_path_y = os.path.join(self.project_dir, *['Survey', 'Receiver', src_filename_y])
                    np.savetxt(rcv_config_path_y,
                               self.rcv_path_y,
                               delimiter=',')
                    # save rcv_path_x and rcv_path_y
                    src_filename = save_win.lineEdit_filename.text() + '.txt'
                    rcv_config_path = os.path.join(self.project_dir, *['Survey', 'Receiver', src_filename])
                    np.savetxt(rcv_config_path,
                               np.concatenate((self.rcv_path_x, self.rcv_path_y), axis=0),
                               delimiter=',')
                    QMessageBox.information(self, 'Saving receiver configuration',
                                            'Current receiver configuration saved.',
                                            QMessageBox.Yes)

    @track_error
    def import_rcv(self):
        receiver_dir, tmp = QFileDialog.getOpenFileName(self,
                                                        "Choose receiver file",
                                                        "*")
        if receiver_dir:
            # show observed points

            # show rcv path points
            rcv_points = np.loadtxt(receiver_dir, delimiter=',')
            # rcv_points1 = np.empty((rcv_points.shape[0] * 2, 3))
            # rcv1 = self.rcv_points1[:, :3]
            # rcv2 = self.rcv_points1[:, 3:]
            self.label_rcvfile.setText(receiver_dir.split('/')[-1])
            self.lineEdit_rcvXmin.setEnabled(False)
            self.lineEdit_rcvXmax.setEnabled(False)
            self.lineEdit_rcvXint.setEnabled(False)
            self.lineEdit_rcvYmin.setEnabled(False)
            self.lineEdit_rcvYmax.setEnabled(False)
            self.lineEdit_rcvYint.setEnabled(False)
            if self.topo_data is None:
                self.table_rcv.points_to_table(rcv_points)
            else:
                reply = QMessageBox.question(self.pushButton_import_rcv,
                                             'Use topo data?',
                                             'Do you want to interpolate path points from the loaded elevation data?',
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.table_rcv.points_to_table(rcv_points)
                    self.update_elevation_rcv(rcv_points)
                else:
                    self.table_rcv.points_to_table(rcv_points)

            QMessageBox.information(self.pushButton_import_rcv,
                                    'Import data',
                                    'Import receiver path data successfully.',
                                    QMessageBox.Yes)

            # # copy file
            # shutil.copy(receiver_dir, os.path.join(self.project_dir, *['Survey', 'Receiver']))

    def rcv_table_init(self):
        self.table_rcv.table_init(0)
        self.label_rcvfile.clear()
        self.lineEdit_rcvXmin.setEnabled(True)
        self.lineEdit_rcvXmax.setEnabled(True)
        self.lineEdit_rcvXint.setEnabled(True)
        self.lineEdit_rcvYmin.setEnabled(True)
        self.lineEdit_rcvYmax.setEnabled(True)
        self.lineEdit_rcvYint.setEnabled(True)
        self.pushButton_save_rcv.setEnabled(True)

    @track_error
    def view_survey(self):
        # open selector dialog
        src_rcv_select_win = DoubleSelectWin([os.path.join(self.project_dir, *['Survey', 'Source']),
                                              os.path.join(self.project_dir, *['Survey', 'Receiver'])],
                                             ['source', 'receiver'])
        src_rcv_select_win.exec()
        if src_rcv_select_win.select_flag:
            src_path = np.loadtxt(src_rcv_select_win.selected_path_left, delimiter=',')
            rcv_path = np.loadtxt(src_rcv_select_win.selected_path_right, delimiter=',')
            self.label_srcfile.setText(src_rcv_select_win.selected_file_left)
            self.label_rcvfile.setText(src_rcv_select_win.selected_file_right)
            self.build_survey(src_path=src_path, rcv_path=rcv_path)

    def view_added_wellpaths(self):
        wellpath_paths, tmp = QFileDialog.getOpenFileNames(self,
                                                      "Choose wellpath points files",
                                                      "*.txt")
        if wellpath_paths:
            for i in range(len(wellpath_paths)):
                wellpath_path = wellpath_paths[i]
                well_points_o = np.loadtxt(wellpath_path, delimiter=',')
                well_points = pv.PolyData(well_points_o)
                self.plotter.add_points(well_points, color='k')

    @track_error_args
    def build_survey(self, src_path, rcv_path):
        x = np.array(rcv_path)
        receiverx = (x[:, 0] + x[:, 3]) / 2
        receivery = (x[:, 1] + x[:, 4]) / 2
        receiverz = (x[:, 2] + x[:, 5]) / 2

        rcv_points = pv.PolyData(np.column_stack((receiverx, receivery, receiverz)))

        self.plotter.add_points(rcv_points, color='b')
        src_line = self.lines_from_points(src_path)
        self.plotter.add_mesh(src_line, color='r')
        # self.ViewWidget.add_bounding_box()
        self.plotter.show_bounds(grid='back', location='outer', all_edges=True)

    def clear_view(self):
        self.plotter.clear()

    @track_error_args
    def lines_from_points(self, points):
        """Given an array of points, make a line set"""
        poly = pv.PolyData()
        poly.points = points
        cells = np.full((len(points) - 1, 3), 2, dtype=np.int_)
        cells[:, 1] = np.arange(0, len(points) - 1, dtype=np.int_)
        cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
        poly.lines = cells
        return poly

    def activate_src_int_setting(self):
        if self.checkBox_srcint.isChecked():
            self.lineEdit_srcint.setEnabled(True)
        else:
            self.lineEdit_srcint.setEnabled(False)

    def loading_finished(self):
        self.topo_data = self.job_worker.topo_data
        QMessageBox.information(self.pushButton_topoBrowser,
                                'Load topography finished!',
                                'Elevation (Z) will be updated by the loaded topography data.',
                                QMessageBox.Yes)
