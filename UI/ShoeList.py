# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShoeList.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from settings.settings import Settings
from PyQt5 import QtCore, QtGui, QtWidgets
import ShoeDetail
import datetime

settings = Settings()

class ShoeDetailWindow(QtWidgets.QMainWindow, ShoeDetail.Ui_ShoeDetail):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

class Ui_ShoeList(object):
    def setupUi(self, ShoeList):
        ShoeList.setObjectName("ShoeList")
        ShoeList.resize(1031, 243)
        ShoeList.setStyleSheet("")
        ShoeList.setWindowModality(QtCore.Qt.ApplicationModal)
        self.shoe_detail_window = ShoeDetailWindow()
        self.shoe_detail_window.parent_window = self
        self.centralwidget = QtWidgets.QWidget(ShoeList)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 1011, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.verticalHeader().setVisible(False)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        ShoeList.setCentralWidget(self.centralwidget)
        self.buttonAdd = QtWidgets.QPushButton(self.centralwidget)
        self.buttonAdd.setGeometry(QtCore.QRect(913, 210, 91, 32))
        self.buttonAdd.setObjectName("buttonAdd")
        self.buttonAdd.clicked.connect(self.add_shoe_detail)
        self.buttonEdit = QtWidgets.QPushButton(self.centralwidget)
        self.buttonEdit.setGeometry(QtCore.QRect(810, 210, 91, 32))
        self.buttonEdit.setObjectName("buttonEdit")
        self.buttonEdit.clicked.connect(self.edit_shoe_detail)
        self.menubar = QtWidgets.QMenuBar(ShoeList)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 22))
        self.menubar.setObjectName("menubar")
        ShoeList.setMenuBar(self.menubar)
        self.insert_shoes()

        self.retranslateUi(ShoeList)
        QtCore.QMetaObject.connectSlotsByName(ShoeList)

    def edit_shoe_detail(self):
        if len(self.tableWidget.selectedIndexes()) > 0:
            row = [x.row() for x in self.tableWidget.selectedIndexes()][-1]
            self.shoe_detail_window.get_shoe_detail(self.tableWidget.item(row, 0).text())
            self.shoe_detail_window.show()

    def add_shoe_detail(self):
        self.shoe_detail_window.reset_shoe_detail()
        self.shoe_detail_window.show()

    def insert_shoes(self):
        self.tableWidget.setRowCount(0)
        for row in settings.database.get_shoe_list_detail():
            row_pos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_pos)
            for idx in range(len(row)):
                if isinstance(row[idx], datetime.datetime):
                    item = row[idx].strftime('%Y-%m-%d')
                elif row[idx] is None:
                    item = ''
                else:
                    item = str(row[idx])
                self.tableWidget.setItem(row_pos, idx, QtWidgets.QTableWidgetItem(item))

    def retranslateUi(self, ShoeList):
        _translate = QtCore.QCoreApplication.translate
        ShoeList.setWindowTitle(_translate("ShoeList", "Shoes"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ShoeList", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ShoeList", "Brand"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("ShoeList", "DateBought"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("ShoeList", "DateRetired"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("ShoeList", "MilesRun"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("ShoeList", "KMRun"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("ShoeList", "AveragePaceMile"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("ShoeList", "AveragePaceKM"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("ShoeList", "LongestRunMile"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("ShoeList", "LongestRunKM"))
        self.buttonAdd.setText(_translate("ShoeList", "Add"))
        self.buttonEdit.setText(_translate("ShoeList", "Edit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ShoeList = QtWidgets.QMainWindow()
    ui = Ui_ShoeList()
    ui.setupUi(ShoeList)
    ShoeList.show()
    sys.exit(app.exec_())

