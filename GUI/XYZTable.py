import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem, QDialog

from UI_init.Ui_tabXYZtable import Ui_xyz_table

class XYZTable(QDialog, Ui_xyz_table):
    def __init__(self, nc, Hheaders):
        super(XYZTable, self).__init__()
        self.setupUi(self)
        self.nc = nc
        self.Hheaders = Hheaders

        self.table_init(0)

    def points_to_table(self, points):
        self.table_init(points.shape[0])
        for i in range(points.shape[1]):
            self.points_to_table_column(points[:, i], i)

    def points_to_table_column(self, vector, ic):
        for i in range(len(vector)):
            self.tableWidget.item(i, ic).setText(str(vector[i]))

    def clear_table_column(self, ic):
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, ic).setText('')

    def table_to_points(self):
        points = np.empty((self.tableWidget.rowCount(), self.tableWidget.columnCount()))
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                points[i, j] = float(self.tableWidget.item(i, j).text())
        return points

    def table_init(self, nr):
        self.tableWidget.setColumnCount(self.nc)
        for j in range(self.nc):
            self.tableWidget.setHorizontalHeaderItem(j, QTableWidgetItem())
            self.tableWidget.horizontalHeaderItem(j).setText(self.Hheaders[j])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.setRowCount(nr)
        for i in range(nr):
            self.initial_one_row(i)

    def initial_one_row(self, i):
        self.tableWidget.setVerticalHeaderItem(i, QTableWidgetItem())
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)
        self.tableWidget.verticalHeader().setMinimumSectionSize(20)
        self.tableWidget.verticalHeaderItem(i).setText((str(i + 1)))
        for j in range(self.nc):
            self.tableWidget.setItem(i, j, QTableWidgetItem())

    def zero_margin(self):
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
