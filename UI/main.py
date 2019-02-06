
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os, json, pyperclip, datetime
from dateutil.relativedelta import relativedelta
from settings.settings import Settings
from VDOT.VDOT import VDOT
from creator.creator import refresh_workouts
import Calendar
import MainMenu
import Diary
import ShoeList
import ShoeDetail

settings = Settings()


class CalendarWindow(QMainWindow, Calendar.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self._current_month = self.current_date.month
        self._current_year = self.current_date.year
        self.generate_calendar(self._current_month, self._current_year)

        self.comboMonth.currentIndexChanged.connect(
            self.combo_change_calendar)
        self.comboYear.currentIndexChanged.connect(
            self.combo_change_calendar)
        self.pushNextMonth.clicked.connect(self.next_month)
        self.pushPrevMonth.clicked.connect(self.prev_month)

    def PrintClick(self, item):
        print('override')
        print(item.item_type, item.item_id)

    def combo_change_calendar(self):
        """On change of the combo boxes, the calendar is regenerated."""
        if (self.comboMonth.currentIndex() + 1 == self._current_month and
                    int(self.comboYear.currentText()) == self._current_year):
            return
        self._current_month = self.comboMonth.currentIndex() + 1
        self._current_year = int(self.comboYear.currentText())
        self.generate_calendar(self._current_month, self._current_year)

    def prev_month(self):
        """Puts the calendar at the previous month."""
        month_index = self.comboMonth.currentIndex()
        year_index = self.comboYear.currentIndex()
        if month_index == 0 and year_index == 0:
            return
        if month_index == 0:
            self.comboMonth.setCurrentIndex(self.comboMonth.count() - 1)
            self.comboYear.setCurrentIndex(year_index - 1)
        else:
            self.comboMonth.setCurrentIndex(month_index - 1)

    def next_month(self):
        """Puts the calendar at the following month."""
        month_index = self.comboMonth.currentIndex()
        year_index = self.comboYear.currentIndex()
        if (month_index == self.comboMonth.count() - 1
                and year_index == self.comboYear.count() - 1):
            return
        if month_index == self.comboMonth.count() - 1:
            self.comboMonth.setCurrentIndex(0)
            self.comboYear.setCurrentIndex(year_index + 1)
        else:
            self.comboMonth.setCurrentIndex(month_index + 1)

    def generate_calendar(self, month, year):
        """Generates the months calendar for the given month and year."""
        start_day = datetime.date(day=1, month=month, year=year)
        end_day = start_day + relativedelta(months=1) - relativedelta(days=1)
        start_day -= relativedelta(days=start_day.isoweekday() - 1)
        end_day += relativedelta(days=7 - end_day.isoweekday())
        weeks = int(((end_day - start_day).days + 1) / 7)
        self.create_calendar(start_day, weeks, month, year)


class DiaryWindow(QMainWindow, Diary.Ui_Diary):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.diary_id = None
        self.DateDiary.setDate(QDate.currentDate())
        self.webView.setUrl(QUrl('https://www.strava.com/activities/1870360336'))
        self.set_run_type_combo()
        self.buttonSave.clicked.connect(self.save_diary)

    def set_run_type_combo(self):
        """Sets the values for the comboRunType."""
        self.comboRunType.clear()
        self.comboRunType.addItem('', 0)
        for i, x in enumerate(settings.database.get_run_types()):
            self.comboRunType.addItem(x[1], x[0])

    def save_diary(self):
        print(self.comboRunType.currentIndex(), str(self.comboRunType.currentText()), self.comboRunType.itemData(self.comboRunType.currentIndex()))
        if self.complete_form():
            self.diary_id = settings.add_diary()

    def complete_form(self):
        """Checks that the form has been completed before saving/editing."""
        pass


class ShoeListWindow(QMainWindow, ShoeList.Ui_ShoeList):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


class Window(QMainWindow, MainMenu.Ui_RunningApp):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.calendar_window = CalendarWindow()
        self.diary_window = DiaryWindow()
        self.shoe_window = ShoeListWindow()
        # Set action for clicking browse button
        self.buttonCalendar.clicked.connect(self.open_calendar)
        self.buttonDiary.clicked.connect(self.open_diary)
        self.buttonShoe.clicked.connect(self.open_shoe_list)

    def open_calendar(self):
        self.calendar_window.show()

    def open_diary(self):
        self.diary_window.show()

    def open_shoe_list(self):
        self.shoe_window.show()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())