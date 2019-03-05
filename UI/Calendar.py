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
    def __init__(self, widget_object, current_day):
        QtWidgets.QListWidget.__init__(self, widget_object)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.context_menu = None
        self.itemClicked.connect(self.item_click)
        self.itemDoubleClicked.connect(self.item_click)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.list_date = current_day

    def set_list_date(self, list_date):
        self.list_date = list_date

    def show_context_menu(self, position):
        self.context_menu = QtWidgets.QMenu()
        if self.currentItem():
            remove_action = self.context_menu.addAction("Remove " + self.currentItem().item_type)
        else:
            remove_action = None
        add_diary_action = self.context_menu.addAction('Add Diary')
        add_race_action = self.context_menu.addAction('Add Race')
        menu_action = self.context_menu.exec_(self.mapToGlobal(position))
        if menu_action == remove_action:
            print('remove')
        elif menu_action == add_diary_action:
            self.add_diary_option()
        elif menu_action == add_race_action:
            self.add_race_option()

    def add_race_option(self):
        print('add race', self.list_date)

    def add_diary_option(self):
        print('add diary', self.list_date)

    def item_click(self, item):
        return (item.item_type, item.item_id)

    def startDrag(self, supported_actions):
        drag = QtGui.QDrag(self)
        mime_data = self.model().mime_data(self.selectedIndexes())
        drag.setMimeData(mime_data)

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
        self.diary_window = None
        self.race_window = None
        self.current_item = None

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
        self.comboMonth.setGeometry(QtCore.QRect(580, 105, 100, 25))
        self.comboMonth.setObjectName(_fromUtf8("comboMonth"))
        for i, month in enumerate(months):
            self.comboMonth.addItem(_fromUtf8(""))
            self.comboMonth.setItemText(i, _translate("MainWindow", month, None))
        self.comboMonth.setCurrentIndex(self.current_date.month - 1)

        self.comboYear = QtWidgets.QComboBox(self.centralwidget)
        self.comboYear.setGeometry(QtCore.QRect(685, 105, 80, 25))
        self.comboYear.setObjectName(_fromUtf8("comboYear"))

        for i, year in enumerate(years):
            self.comboYear.addItem(_fromUtf8(""))
            self.comboYear.setItemText(i, _translate("MainWindow", year, None))
        year_index = self.comboYear.findText(str(self.current_date.year))
        self.comboYear.setCurrentIndex(year_index)

        self.pushNextMonth = QtWidgets.QPushButton(self.centralwidget)
        self.pushNextMonth.setGeometry(QtCore.QRect(770, 100, 60, 25))
        self.pushNextMonth.setObjectName(_fromUtf8("pushNextMonth"))
        self.pushNextMonth.setText(_translate("MainWindow", "Next", None))
        self.pushPrevMonth = QtWidgets.QPushButton(self.centralwidget)
        self.pushPrevMonth.setGeometry(QtCore.QRect(515, 100, 60, 25))
        self.pushPrevMonth.setObjectName(_fromUtf8("pushPrevMonth"))
        self.pushPrevMonth.setText(_translate("MainWindow", "Prev", None))
        self.comboMonth.count()

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

    def set_diary_window(self, window):
        self.diary_window = window

    def set_race_window(self, window):
        self.race_window = window

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
                self.add_calendar_lists(name, current_day.month == month, current_day)
                self.add_calendar_labels(name)

            self.add_calendar_layouts(name)
            self.add_calendar_to_layout(name)

            self.gridLayout.setColumnStretch((day+1) % 8, 1)
            self.gridLayout.addLayout(self.layouts[name], week, day, 1, 1)

    def add_calendar_layouts(self, day):
        """Adds layout for the calendar day."""
        self.layouts[day] = QtWidgets.QVBoxLayout()
        self.layouts[day].setObjectName(_fromUtf8("vlay" + day))

    def add_calendar_lists(self, day, current, current_day):
        """Adds the list for the calendar day."""
        self.lists[day] = CustomList(self.verticalLayoutWidget, current_day)
        self.lists[day].setObjectName(_fromUtf8(day))
        self.lists[day].setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.lists[day].setDefaultDropAction(QtCore.Qt.MoveAction)
        self.lists[day].itemClicked.connect(self.set_current_item)
        self.lists[day].itemDoubleClicked.connect(self.show_item_window)
        self.lists[day].add_race_option = self.redefine_context_menu_add_race(self.lists[day])
        self.lists[day].add_diary_option = self.redefine_context_menu_add_diary(self.lists[day])
        if not current:
            self.lists[day].setEnabled(False)
        else:
            self.add_calendar_items(day)

    def add_calendar_items(self, day):
        """Adds calendar items to the day view."""
        for i, item in enumerate([x for x in self.calendar if x[2].replace(hour=0, minute=0, second=0) == datetime.datetime.strptime(day, '%Y%m%d')]):
            print(item)
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

    def show_item_window(self, item):
        self.set_current_item(item)
        if not self.current_item:
            return
        if self.current_item[0] == 'Diary':
            self.diary_window.get_diary_details(self.current_item[1])
            self.diary_window.show()
        elif self.current_item[0] == 'Race':
            self.race_window.get_race_details(self.current_item[1])
            self.race_window.show()

    def set_current_item(self, item):
        self.current_item = (item.item_type, item.item_id)

    def redefine_context_menu_add_race(self, list_widget):
        def func():
            self.race_window.reset_form(list_widget.list_date)
            self.race_window.show()
        return func

    def redefine_context_menu_add_diary(self, list_widget):
        def func():
            self.diary_window.reset_form(list_widget.list_date)
            self.diary_window.show()
        return func


def set_list_widget_colour(list_type):
    """Returns the colour for that list widget type given."""
    colours = {
        'Race': '#7fc97f',
        'Workout': '#beaed4',
        'Diary': '#fdc086'
    }
    return colours[list_type]
