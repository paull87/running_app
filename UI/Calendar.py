# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Calendar.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from dateutil.relativedelta import relativedelta
from settings.settings import Settings

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

settings = Settings()

weekdays = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
    ''
]

months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]
years = [
    '2015',
    '2016',
    '2017',
    '2018',
    '2019',
    '2020',
    '2021'
]

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)



class CustomListItem(QtWidgets.QListWidgetItem):
    def __init__(self):
        QtWidgets.QListWidgetItem.__init__(self)
        self.item_type = None
        self.item_id = None

    def set_item_properties(self, properties):
        """Sets the custom item type and id"""
        self.item_type, self.item_id = properties


class CustomList(QtWidgets.QListWidget):
    def __init__(self, *args):
        QtWidgets.QListWidget.__init__(self, *args)
        self.itemClicked.connect(self.item_click)

    def item_click(self, item):
        return (item.item_type, item.item_id)

    def startDrag(self, supportedActions):
        drag = QtGui.QDrag(self)
        mimeData = self.model().mimeData(self.selectedIndexes())
        drag.setMimeData(mimeData)

        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            for item in self.selectedItems():
                self.takeItem(self.row(item))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.ignore()
        elif event.source().currentItem().item_type != 'Workout':  # Only allow Workouts to be moved
            event.ignore()
        else:
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.ignore()
        else:
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.ignore()
        if isinstance(event.source(), CustomList):
            moved_item = event.source().takeItem(event.source().currentRow())
            self.addItem(moved_item)
        else:
            event.ignore()

    def dropMimeData(self, index, mimedata, action):
        super(CustomList, self).dropMimeData(index, mimedata, action)
        return True


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 900)
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.lists = dict()
        self.labels = dict()
        self.layouts = dict()
        self.calendar = None
        self.calendar_items = dict()

        self.current_date = datetime.date.today()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 150, 900, 700))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.labeldays = dict()
        for day in weekdays:
            self.labeldays[day] = QtWidgets.QLabel(self.verticalLayoutWidget)
            self.labeldays[day].setObjectName(_fromUtf8("lbl" + day))
            self.labeldays[day].setText(_translate("MainWindow", day, None))
            self.horizontalLayout.addWidget(self.labeldays[day])

        self.comboMonth = QtWidgets.QComboBox(self.centralwidget)
        self.comboMonth.setGeometry(QtCore.QRect(580, 100, 69, 22))
        self.comboMonth.setObjectName(_fromUtf8("comboMonth"))
        for i, month in enumerate(months):
            self.comboMonth.addItem(_fromUtf8(""))
            self.comboMonth.setItemText(i, _translate("MainWindow", month, None))
        self.comboMonth.setCurrentIndex(self.current_date.month - 1)

        self.comboYear = QtWidgets.QComboBox(self.centralwidget)
        self.comboYear.setGeometry(QtCore.QRect(650, 100, 69, 22))
        self.comboYear.setObjectName(_fromUtf8("comboYear"))

        for i, year in enumerate(years):
            self.comboYear.addItem(_fromUtf8(""))
            self.comboYear.setItemText(i, _translate("MainWindow", year, None))
        year_index = self.comboYear.findText(str(self.current_date.year))
        self.comboYear.setCurrentIndex(year_index)

        self.pushNextMonth = QtWidgets.QPushButton(self.centralwidget)
        self.pushNextMonth.setGeometry(QtCore.QRect(720, 100, 51, 22))
        self.pushNextMonth.setObjectName(_fromUtf8("pushNextMonth"))
        self.pushNextMonth.setText(_translate("MainWindow", "Next", None))
        self.pushPrevMonth = QtWidgets.QPushButton(self.centralwidget)
        self.pushPrevMonth.setGeometry(QtCore.QRect(530, 100, 51, 22))
        self.pushPrevMonth.setObjectName(_fromUtf8("pushPrevMonth"))
        self.pushPrevMonth.setText(_translate("MainWindow", "Prev", None))
        self.comboMonth.count()
        #self.comboMonth.raise_()
        #self.comboYear.raise_()
        #self.pushNextMonth.raise_()
        #self.pushPrevMonth.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def clear_calendar(self):
        for layout in self.layouts.values():
            while layout.count():
                item = layout.takeAt(0)
                item.widget().deleteLater()
            #for list_widget in self.lists.values():
            #    layout.removeWidget(list_widget)
            #for label in self.labels.values():
            #    layout.removeWidget(label)
            self.gridLayout.removeItem(layout)
            layout.deleteLater()
        self.lists.clear()
        self.layouts.clear()
        self.labels.clear()
        self.calendar_items.clear()

    def create_calendar(self, start_date, weeks, month, year):
        self.clear_calendar()
        self.calendar = settings.get_calendar(month, year)
        fmt = 'W{0}D{1}'
        for day, week in [(d, w) for w in range(weeks) for d in range(8)]:
            current_day = start_date + relativedelta(days=(7 * week) + day)
            if day == 7:
                name = 'W{0}Weekly'.format(week + 1)
                self.add_calendar_labels(name)
                self.add_calendar_labels(name + 'Summary', True)
                #self.add_calendar_lists(name, current_day.month == month)
            else:
                # name = fmt.format(week + 1, day + 1)
                name = current_day.strftime('%Y%m%d')
                self.add_calendar_lists(name, current_day.month == month)
                self.add_calendar_labels(name)

            self.add_calendar_layouts(name)
            self.add_calendar_to_layout(name)

            self.gridLayout.setColumnStretch((day+1) % 8, 1)
            self.gridLayout.addLayout(self.layouts[name], week, day, 1, 1)

    def add_calendar_layouts(self, day):
        """Adds layout for the calendar day."""
        self.layouts[day] = QtWidgets.QVBoxLayout()
        self.layouts[day].setObjectName(_fromUtf8("vlay" + day))

    def add_calendar_lists(self, day, current):
        """Adds the list for the calendar day."""
        self.lists[day] = CustomList(self.verticalLayoutWidget)
        self.lists[day].setObjectName(_fromUtf8(day))
        self.lists[day].setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.lists[day].setDefaultDropAction(QtCore.Qt.MoveAction)
        self.lists[day].itemClicked.connect(self.PrintClick)
        if not current:
            self.lists[day].setEnabled(False)
        else:
            self.add_calendar_items(day)


    def add_calendar_items(self, day):
        """Adds calendar items to the day view."""
        for i, item in enumerate([x for x in self.calendar if x[2] == datetime.datetime.strptime(day, '%Y%m%d')]):
            item_name = '{0}\n{3}'.format(*item)
            list_item = '{0}_{1}'.format(*item)
            self.calendar_items[list_item] = CustomListItem()
            self.calendar_items[list_item].setText(_translate("MainWindow", item_name, None))
            self.calendar_items[list_item].set_item_properties(list_item.split('_'))
            self.calendar_items[list_item].setBackground(QtGui.QColor(set_list_widget_colour(item[0])))
            self.lists[day].addItem(self.calendar_items[list_item])

    def add_calendar_to_layout(self, day):
        """Adds the calendar label and list to the days layout."""
        self.layouts[day].addWidget(self.labels[day])
        if 'Weekly' in day:
            self.layouts[day].addWidget(self.labels[day + 'Summary'])
        else:
            self.layouts[day].addWidget(self.lists[day])

    def add_calendar_labels(self, day, summary=False):
        """Adds the calendar day labels and summary ."""
        if summary:
            label_text = '<b>Distance</b><br>0.0<br><b>Time</b><br>00:00:00'
        elif 'Weekly' in day:
            label_text = ''
        else:
            label_text = day[-2:].lstrip('0')

        self.labels[day] = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labels[day].setObjectName(_fromUtf8("lbl" + day))
        self.labels[day].setText(_translate("MainWindow", label_text, None))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Calendar", None))

    def PrintClick(self, item):
        pass

def set_list_widget_colour(list_type):
    """Returns the colour for that list widget type given."""
    colours = {
        'Race': '#7fc97f',
        'Workout': '#beaed4',
        'Diary': '#fdc086'
    }

    return colours[list_type]