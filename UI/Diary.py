# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\PythonScripts\FitnessApp\UI\Diary.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import pyqtgraph
from settings.settings import Settings
from settings.converters import calculate_pace, calculate_speed, convert_distance, dec, time_to_string, convert_weight
from settings.strava import Strava
import datetime
import UI.stylesheets as stylesheets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
import seaborn
import matplotlib
import pandas
import numpy

matplotlib.use('QT5Agg')
seaborn.set()
seaborn.set_style('white', {
    'axes.spines.bottom': False,
    'axes.spines.left': False,
    'axes.spines.right': False,
    'axes.spines.top': False,})
#seaborn.despine(top=True, right=True, left=True, bottom=True)


settings = Settings()
strava = Strava()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class PlotCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = PlotCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class Ui_Diary(object):
    def setupUi(self, Diary):
        Diary.setObjectName(_fromUtf8("Diary"))
        Diary.resize(800, 600)
        Diary.setStyleSheet(_fromUtf8(""))
        Diary.setWindowModality(QtCore.Qt.ApplicationModal)
        self.diary_id = None
        self.centralwidget = QtWidgets.QWidget(Diary)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.dateDiary = QtWidgets.QDateEdit(self.centralwidget)
        self.dateDiary.setGeometry(QtCore.QRect(50, 50, 120, 25))
        self.dateDiary.setCalendarPopup(True)
        self.dateDiary.setObjectName(_fromUtf8("DateDiary"))
        self.dateDiary.dateChanged.connect(self.update_workout_and_race)

        self.timeDiary = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeDiary.setGeometry(QtCore.QRect(175, 50, 60, 25))
        self.timeDiary.setCalendarPopup(False)
        self.timeDiary.setObjectName(_fromUtf8("timeDiary"))
        self.timeDiary.setDisplayFormat('HH:mm')

        self.timeRunLength = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeRunLength.setGeometry(QtCore.QRect(50, 80, 80, 25))
        self.timeRunLength.setCalendarPopup(False)
        self.timeRunLength.setObjectName(_fromUtf8("timeRunLength"))
        self.timeRunLength.setDisplayFormat('HH:mm:ss')

        self.comboRunType = QtWidgets.QComboBox(self.centralwidget)
        self.comboRunType.setGeometry(QtCore.QRect(45, 110, 120, 30))
        self.comboRunType.setObjectName(_fromUtf8("comboRunType"))

        self.comboShoe = QtWidgets.QComboBox(self.centralwidget)
        self.comboShoe.setGeometry(QtCore.QRect(45, 140, 200, 30))
        self.comboShoe.setObjectName(_fromUtf8("comboShoe"))

        self.lineDistance = QtWidgets.QLineEdit(self.centralwidget)
        self.lineDistance.setGeometry(QtCore.QRect(50, 170, 120, 25))
        self.lineDistance.setObjectName(_fromUtf8("lineDistance"))

        self.comboDistance = QtWidgets.QComboBox(self.centralwidget)
        self.comboDistance.setGeometry(QtCore.QRect(175, 170, 70, 30))
        self.comboDistance.setObjectName(_fromUtf8("comboDistance"))
        self.comboDistance.addItem(_fromUtf8(""))
        self.comboDistance.addItem(_fromUtf8(""))
        self.comboDistance.currentIndexChanged.connect(self.distance_combo_change)

        self.lineSpeed = QtWidgets.QLineEdit(self.centralwidget)
        self.lineSpeed.setGeometry(QtCore.QRect(50, 200, 120, 25))
        self.lineSpeed.setObjectName(_fromUtf8("lineSpeed"))

        self.comboSpeed = QtWidgets.QComboBox(self.centralwidget)
        self.comboSpeed.setGeometry(QtCore.QRect(175, 200, 75, 30))
        self.comboSpeed.setObjectName(_fromUtf8("comboSpeed"))
        self.comboSpeed.addItem(_fromUtf8(""))
        self.comboSpeed.addItem(_fromUtf8(""))
        self.comboSpeed.currentIndexChanged.connect(self.speed_combo_change)

        self.linePace = QtWidgets.QLineEdit(self.centralwidget)
        self.linePace.setGeometry(QtCore.QRect(50, 230, 120, 25))
        self.linePace.setObjectName(_fromUtf8("linePace"))

        self.comboPace = QtWidgets.QComboBox(self.centralwidget)
        self.comboPace.setGeometry(QtCore.QRect(175, 230, 95, 30))
        self.comboPace.setObjectName(_fromUtf8("comboPace"))
        self.comboPace.addItem(_fromUtf8(""))
        self.comboPace.addItem(_fromUtf8(""))
        self.comboPace.currentIndexChanged.connect(self.pace_combo_change)

        self.lineAvgHR = QtWidgets.QLineEdit(self.centralwidget)
        self.lineAvgHR.setGeometry(QtCore.QRect(50, 260, 80, 25))
        self.lineAvgHR.setObjectName(_fromUtf8("lineAvgHR"))

        self.lineNotes = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNotes.setGeometry(QtCore.QRect(50, 290, 280, 100))
        self.lineNotes.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lineNotes.setObjectName(_fromUtf8("lineNotes"))

        self.comboEffort = QtWidgets.QComboBox(self.centralwidget)
        self.comboEffort.setGeometry(QtCore.QRect(45, 390, 80, 30))
        self.comboEffort.setObjectName(_fromUtf8("comboEffort"))

        self.comboRating = QtWidgets.QComboBox(self.centralwidget)
        self.comboRating.setGeometry(QtCore.QRect(150, 390, 80, 30))
        self.comboRating.setObjectName(_fromUtf8("comboRating"))

        self.lineWeight = QtWidgets.QLineEdit(self.centralwidget)
        self.lineWeight.setGeometry(QtCore.QRect(50, 420, 70, 25))
        self.lineWeight.setObjectName(_fromUtf8("lineWeight"))

        self.comboWeight = QtWidgets.QComboBox(self.centralwidget)
        self.comboWeight.setGeometry(QtCore.QRect(120, 420, 60, 30))
        self.comboWeight.setObjectName(_fromUtf8("comboWeight"))
        for item in ['lb', 'kg']:
            self.comboWeight.addItem(item)
        self.comboWeight.currentIndexChanged.connect(self.weight_combo_change)

        self.lineRestingHR = QtWidgets.QLineEdit(self.centralwidget)
        self.lineRestingHR.setGeometry(QtCore.QRect(200, 420, 70, 25))
        self.lineRestingHR.setObjectName(_fromUtf8("lineRestingHR"))

        self.comboRace = QtWidgets.QComboBox(self.centralwidget)
        self.comboRace.setGeometry(QtCore.QRect(370, 50, 140, 30))
        self.comboRace.setObjectName(_fromUtf8("comboRace"))

        self.comboWorkout = QtWidgets.QComboBox(self.centralwidget)
        self.comboWorkout.setGeometry(QtCore.QRect(370, 80, 140, 30))
        self.comboWorkout.setObjectName(_fromUtf8("comboWorkout"))

        self.lineStravaID = QtWidgets.QLineEdit(self.centralwidget)
        self.lineStravaID.setGeometry(QtCore.QRect(370, 130, 90, 25))
        self.lineStravaID.setObjectName(_fromUtf8("lineStravaID"))

        self.lineIntensityPointsHR = QtWidgets.QLineEdit(self.centralwidget)
        self.lineIntensityPointsHR.setGeometry(QtCore.QRect(370, 160, 80, 25))
        self.lineIntensityPointsHR.setObjectName(_fromUtf8("lineIntensityPointsHR"))

        self.lineIntensityPointsPace = QtWidgets.QLineEdit(self.centralwidget)
        self.lineIntensityPointsPace.setGeometry(QtCore.QRect(470, 160, 80, 25))
        self.lineIntensityPointsPace.setObjectName(_fromUtf8("lineIntensityPointsPace"))

        self.buttonSave = QtWidgets.QPushButton(self.centralwidget)
        self.buttonSave.setGeometry(QtCore.QRect(100, 480, 75, 30))
        self.buttonSave.setObjectName(_fromUtf8("buttonSave"))
        self.buttonSave.clicked.connect(self.save_diary)

        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(370, 200, 380, 300))
        self.webView.setGeometry(QtCore.QRect(1370, 1200, 380, 300))
        self.webView.setObjectName(_fromUtf8("webView"))

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(530, 390, 264, 155))
        self.calendarWidget.setStyleSheet(_fromUtf8(stylesheets.calendar_popup))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        Diary.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Diary)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Diary.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Diary)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Diary.setStatusBar(self.statusbar)
        self.dateDiary.setCalendarWidget(self.calendarWidget)

        self.canvasWidget = PlotWidget(self.centralwidget)
        self.canvasWidget.setGeometry(QtCore.QRect(370, 200, 380, 300))

        icon_back = QtGui.QIcon()
        icon_back.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-back-26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon_forward = QtGui.QIcon()
        icon_forward.addPixmap(QtGui.QPixmap(_fromUtf8(":/MenuImages/icons8-forward-26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        for child in self.calendarWidget.children():
            for c in child.children():
                if c.objectName() == 'qt_calendar_prevmonth':
                    c.setIcon(icon_back)
                    #c.setText(_translate("Diary", "P", None))
                if c.objectName() == 'qt_calendar_nextmonth':
                    c.setIcon(icon_forward)
                    #c.setText(_translate("Diary", "N", None))

        self.comboEffort.addItem('Effort')
        self.comboRating.addItem('Rating')
        for i in range(5):
            self.comboEffort.addItem(str(i + 1))
            self.comboRating.addItem(str(i + 1))

        self.retranslateUi(Diary)
        self.reset_form()

        self.lineDistance.textChanged.connect(self.calculate_fields)
        self.timeRunLength.timeChanged.connect(self.calculate_fields)
        self.lineWeight.textChanged.connect(self.calculate_fields)
        self.lineStravaID.textChanged.connect(self.strava_updates)

        QtCore.QMetaObject.connectSlotsByName(Diary)

    def plot_laps(self):
        cols = ['LapID', 'StravaID', 'LapStartDate', 'LapTime', 'DistanceMiles', 'DistanceKM', 'SpeedMPH', 'SpeedKPH',
                'PaceMiles', 'PaceKM', 'AverageHR', 'IntensityPointsHR', 'IntensityPointsPace']
        measure = 'PaceMiles'
        laps = pandas.DataFrame(self.strava_laps, columns=cols)
        laps.IntensityPointsHR = laps.IntensityPointsHR.astype('float64')
        laps[measure] = laps[measure].astype('float64')
        self.canvasWidget.canvas.ax.get_yaxis().set_visible(False)
        self.canvasWidget.canvas.ax.get_xaxis().set_visible(False)
        self.canvasWidget.canvas.ax.clear()
        self.canvasWidget.setHidden(False)
        colors = seaborn.color_palette("Blues", len(self.strava_laps))
        rank = laps.IntensityPointsHR.argsort().argsort()
        seaborn.barplot(x=measure, y=laps.index, data=laps, orient="h", color='b',
                        ax=self.canvasWidget.canvas.ax, palette=numpy.array(colors)[rank])
        self.canvasWidget.canvas.draw()

    def distance_combo_change(self):
        if self.distance_miles is None:
            return
        if self.comboDistance.currentText() == 'Mile':
            self.lineDistance.setText(str(dec(self.distance_miles, 2)))
        else:
            self.lineDistance.setText(str(dec(self.distance_km, 2)))

    def weight_combo_change(self):
        if self.weight_lb is None:
            return
        if self.comboWeight.currentText() == 'lb':
            self.lineWeight.setText(str(dec(self.weight_lb, 2)))
        else:
            self.lineWeight.setText(str(dec(self.weight_kg, 2)))

    def pace_combo_change(self):
        if self.pace_miles is None:
            return
        if self.comboPace.currentText() == 'Mile/min':
            self.linePace.setText(time_to_string(self.pace_miles, '{hours:02d}:{minutes:02d}:{seconds:02d}'))
        else:
            self.linePace.setText(time_to_string(self.pace_km, '{hours:02d}:{minutes:02d}:{seconds:02d}'))

    def speed_combo_change(self):
        if self.speed_miles is None:
            return
        if self.comboSpeed.currentText() == 'mph':
            self.lineSpeed.setText(str(self.speed_miles))
        else:
            self.lineSpeed.setText(str(self.speed_km))

    def calculate_fields(self):
        if self.timeRunLength.time() != QtCore.QTime(0, 0, 0):
            self.run_length_time = (datetime.datetime.combine(datetime.date.min,
                                       self.timeRunLength.time().toPyTime()) - datetime.datetime.min)
        if (self.run_length_time.total_seconds() > 0
            and self.lineDistance.text() != ''
            and dec(self.lineDistance.text()) > 0):
            if self.comboDistance.currentText() == 'Mile':
                self.distance_miles = dec(self.lineDistance.text())
                self.distance_km = convert_distance(self.distance_miles, 'mile', 'km')
            else:
                self.distance_km = dec(self.lineDistance.text())
                self.distance_miles = convert_distance(self.distance_km, 'km', 'mile')
            self.pace_miles = calculate_pace(self.run_length_time, self.distance_miles, 'mile')
            self.pace_km = calculate_pace(self.run_length_time, self.distance_km, 'km')
            self.pace_combo_change()
            self.speed_miles = calculate_speed(self.distance_miles, self.run_length_time)
            self.speed_km = calculate_speed(self.distance_km, self.run_length_time)
            self.speed_combo_change()
        if self.lineWeight.text() != '':
            if self.comboWeight.currentText() == 'lb':
                self.weight_lb = dec(self.lineWeight.text())
                self.weight_kg = convert_weight(self.weight_lb, 'lb', 'kg')
            else:
                self.weight_kg = dec(self.lineWeight.text())
                self.weight_lb = convert_weight(self.weight_kg, 'kg', 'lb')

    def reset_form(self):
        self.timeDiary.setTime(QtCore.QTime(0, 0))
        self.dateDiary.setDate(QtCore.QDate.currentDate())
        self.timeRunLength.setTime(QtCore.QTime(0, 0, 0))
        self.set_shoe_list_combo()
        self.set_run_type_combo()
        self.comboEffort.setCurrentIndex(0)
        self.comboRating.setCurrentIndex(0)
        self.lineDistance.clear()
        self.lineAvgHR.clear()
        self.lineSpeed.clear()
        self.linePace.clear()
        self.lineRestingHR.clear()
        self.lineNotes.clear()
        self.lineWeight.clear()
        self.lineStravaID.clear()
        self.lineIntensityPointsHR.clear()
        self.lineIntensityPointsPace.clear()
        self.distance_miles = None
        self.distance_km = None
        self.speed_miles = None
        self.speed_km = None
        self.pace_miles = None
        self.pace_km = None
        self.weight_kg = None
        self.weight_lb = None
        self.run_length_time = datetime.timedelta(0)
        self.strava_laps = list()
        self.canvasWidget.setHidden(True)

    def get_diary_details(self, diary_id):
        self.reset_form()
        self.diary_id = diary_id
        diary = settings.database.get_diary_entry(diary_id)
        diary_date = diary[1]
        self.dateDiary.setDate(QtCore.QDate(diary_date.year, diary_date.month, diary_date.day))
        self.timeDiary.setTime(QtCore.QTime(diary_date.hour, diary_date.minute))
        self.timeRunLength.setTime(QtCore.QTime(0, 0, 0).addSecs(diary[2]))
        self.comboRunType.setCurrentIndex(self.get_run_type_combo_id(diary[3]))
        self.lineDistance.setText(str(diary[4]))
        self.lineSpeed.setText(str(diary[6]))
        self.linePace.setText(str(diary[8]))
        self.lineAvgHR.setText(str(diary[10]) if diary[10] else None)
        self.comboShoe.setCurrentIndex(self.get_shoe_list_combo_id(diary[11]))
        self.comboWorkout.setCurrentIndex(self.get_workout_combo_id(diary[12]))
        self.comboEffort.setCurrentIndex(diary[13] if diary[13] else 0)
        self.comboRating.setCurrentIndex(diary[14] if diary[14] else 0)
        self.comboRace.setCurrentIndex(self.get_race_combo_id((diary[15])))
        self.lineStravaID.setText(str(diary[16]) if diary[16] else None)
        self.lineIntensityPointsHR.setText(str(diary[17]) if diary[17] else None)
        self.lineIntensityPointsPace.setText(str(diary[18]) if diary[18] else None)
        self.lineNotes.setText(diary[19])
        self.get_health_stats_details()

    def get_health_stats_details(self):
        diary_date = datetime.datetime.combine(self.dateDiary.date().toPyDate(), datetime.datetime.min.time())
        health_stats = settings.database.get_health_stats(diary_date)
        if health_stats is not None:
            self.lineWeight.setText(str(health_stats[2]))
            self.lineRestingHR.setText(str(health_stats[3]))

    def get_run_type_combo_id(self, id):
        combo_id = self.comboRunType.findData(id)
        combo_id = 0 if combo_id == -1 else combo_id
        return combo_id

    def get_shoe_list_combo_id(self, id):
        combo_id = self.comboShoe.findData(id)
        combo_id = 0 if combo_id == -1 else combo_id
        return combo_id

    def get_workout_combo_id(self, id):
        combo_id = self.comboWorkout.findData(id)
        combo_id = 0 if combo_id == -1 else combo_id
        return combo_id

    def get_race_combo_id(self, id):
        combo_id = self.comboRace.findData(id)
        combo_id = 0 if combo_id == -1 else combo_id
        return combo_id

    def set_run_type_combo(self):
        """Sets the values for the comboRunType."""
        self.comboRunType.clear()
        self.comboRunType.addItem('', 0)
        for i, x in enumerate(settings.database.get_run_types()):
            self.comboRunType.addItem(x[1], x[0])

    def set_shoe_list_combo(self):
        """Sets the values for the comboShoe."""
        self.comboShoe.clear()
        self.comboRunType.addItem('', 0)
        for shoe_id, shoe_name, _ in settings.database.get_shoe_list():
            self.comboShoe.addItem(shoe_name, shoe_id)

    def set_race_combo(self):
        """Sets the values for the comboRace."""
        start_date = datetime.datetime.combine(self.dateDiary.date().toPyDate(), datetime.datetime.min.time())
        end_date = start_date + datetime.timedelta(days=1)
        self.comboRace.clear()
        self.comboRace.addItem('Race', 0)
        races = [x for x in settings.database.get_calendar_range(start_date, end_date) if x[0] == 'Race']
        for race in races:
            self.comboRace.addItem(race[3], race[1])

    def set_workout_combo(self):
        """Sets the values for the comboWorkout."""
        start_date = datetime.datetime.combine(self.dateDiary.date().toPyDate(), datetime.datetime.min.time())
        end_date = start_date + datetime.timedelta(days=10)
        start_date = start_date - datetime.timedelta(days=10)
        self.comboWorkout.clear()
        self.comboWorkout.addItem('Workout', 0)
        workouts = [x for x in settings.database.get_calendar_range(start_date, end_date) if x[0] == 'Workout']
        for workout in workouts:
            self.comboWorkout.addItem(workout[3], workout[1])

    def update_workout_and_race(self):
        """Updates the workout and race combos in line with the date change."""
        self.set_race_combo()
        self.set_workout_combo()

    def convert_diary_entry(self):
         return (
             self.diary_id,
             datetime.datetime.combine(self.dateDiary.date().toPyDate(), self.timeDiary.time().toPyTime()),
             self.run_length_time.total_seconds(),
             self.comboRunType.itemData(self.comboRunType.currentIndex()),
             str(self.distance_miles),
             str(self.distance_km),
             str(self.speed_miles),
             str(self.speed_km),
             self.pace_miles.total_seconds(),
             self.pace_km.total_seconds(),
             self.lineAvgHR.text(),
             self.comboShoe.itemData(self.comboShoe.currentIndex()),
             self.comboWorkout.itemData(self.comboWorkout.currentIndex()),
             None if self.comboEffort.currentIndex() == 0 else self.comboEffort.currentText(),
             None if self.comboRating.currentIndex() == 0 else self.comboRating.currentText(),
             self.comboRace.itemData(self.comboRace.currentIndex()),
             self.lineStravaID.text(),
             self.lineIntensityPointsHR.text(),
             self.lineIntensityPointsPace.text(),
             self.lineNotes.text(),
             False
         )

    def convert_health_stats(self):
        return (
            datetime.datetime.combine(self.dateDiary.date().toPyDate(), datetime.datetime.min.time()),
            str(self.weight_kg),
            str(self.weight_lb),
            self.lineRestingHR.text()
        )

    def complete_form(self):
        """Checks that the form has been completed before saving/editing."""
        return (len(self.lineDistance.text()) > 0
                and len(self.lineSpeed.text()) > 0
                and len(self.linePace.text()) > 0
                and len(self.lineAvgHR.text()) > 0
                )

    def complete_weight_form(self):
        """Checks if the weight section is populated."""
        return (len(self.lineWeight.text()) > 0
                and len(self.lineRestingHR.text()) > 0
                )

    def strava_updates(self):
        if self.lineStravaID.text() == '':
            return
        self.webView.setUrl(QtCore.QUrl(f'https://www.strava.com/activities/{self.lineStravaID.text()}'))
        self.get_strava_laps()
        self.calculate_intensity_points_hr()
        self.plot_laps()

    def calculate_intensity_points_hr(self):
        points = 0
        points += sum([dec(x[-2]) for x in self.strava_laps])
        self.lineIntensityPointsHR.setText(str(points))

    def get_strava_laps(self):
        """Saves the list of strava laps for the current strava_id."""
        self.strava_laps = list()
        strava_id = self.lineStravaID.text()
        try:
            for lap in strava.get_laps(strava_id):
                self.strava_laps.append((
                    lap.id, strava_id, lap.start_date_local, lap.moving_time.total_seconds(), str(dec(lap.distance_miles, 4)),
                    str(dec(lap.distance_km, 4)), str(lap.speed_mile), str(lap.speed_km), lap.pace_mile.total_seconds(),
                    lap.pace_km.total_seconds(), lap.average_heartrate,
                    str(settings.calculate_intensity_points(lap.average_heartrate, lap.moving_time)), None)
                )
        except:
            return

    def save_strava_laps(self):
        if self.strava_laps:
            for lap in self.strava_laps:
                settings.database.add_strava_lap(lap)

    def save_diary(self):
        if self.complete_form():
            self.diary_id = settings.database.add_diary_entry(self.convert_diary_entry())
        if self.complete_weight_form():
            settings.database.add_health_stats(self.convert_health_stats())
        self.save_strava_laps()

    def retranslateUi(self, Diary):
        Diary.setWindowTitle(_translate("Diary", "MainWindow", None))
        self.lineDistance.setPlaceholderText(_translate("Diary", "Distance", None))
        self.lineSpeed.setPlaceholderText(_translate("Diary", "Speed", None))
        self.comboDistance.setItemText(0, _translate("Diary", "Mile", None))
        self.comboDistance.setItemText(1, _translate("Diary", "KM", None))
        self.linePace.setPlaceholderText(_translate("Diary", "Pace", None))
        self.comboSpeed.setItemText(0, _translate("Diary", "mph", None))
        self.comboSpeed.setItemText(1, _translate("Diary", "kmph", None))
        self.comboPace.setItemText(0, _translate("Diary", "Mile/min", None))
        self.comboPace.setItemText(1, _translate("Diary", "KM/min", None))
        self.lineAvgHR.setPlaceholderText(_translate("Diary", "Avg HR", None))
        self.lineNotes.setPlaceholderText(_translate("Diary", "Commet...", None))
        self.lineWeight.setPlaceholderText(_translate("Diary", "Weight", None))
        self.lineRestingHR.setPlaceholderText(_translate("Diary", "Rest HR", None))
        self.buttonSave.setText(_translate("Diary", "Save", None))
        self.lineStravaID.setPlaceholderText(_translate("Diary", "StravaID", None))
        self.lineIntensityPointsHR.setPlaceholderText(_translate("Diary", "HR Intensity", None))
        self.lineIntensityPointsPace.setPlaceholderText(_translate("Diary", "Pace Intensity", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Diary = QtWidgets.QMainWindow()
    ui = Ui_Diary()
    ui.setupUi(Diary)
    Diary.show()
    sys.exit(app.exec_())

