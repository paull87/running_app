from PyQt5 import QtCore, QtWidgets, QtGui
from settings.settings import Settings
from settings.converters import dec
import settings.sql_queries as sql_queries
import datetime
import pandas
import numpy
import functools

from PyQt5.QtChart import *
from PyQt5.QtGui import *


settings = Settings()

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class UiStats(object):

    # def __init__(self):
    #     self.race_id = None
    #     self.central_widget = None
    #     self.date_race = None
    #     self.combo_race_name = None
    #     self.combo_race_distance = None
    #     self.time_goal = None
    #     self.time_actual = None
    #     self.button_save = None
    #     self.menu_bar = None
    #     self.status_bar = None

    def setup_ui(self, stats):
        stats.resize(1000, 1000)
        stats.setWindowModality(QtCore.Qt.ApplicationModal)
        stats.setWindowTitle(_translate("Stats", "Stats", None))
        self.central_widget = QtWidgets.QWidget(stats)
        self._current_year = 0
        self._current_stat = ''

        self.chartView = QChartView(self.central_widget)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView.setGeometry(QtCore.QRect(50, 50, 500, 500))
        self.chartView.setContentsMargins(0, 0, 0, 0)

        self.label_result = QtWidgets.QLabel(self.central_widget)
        self.label_result.setGeometry(100, 80, 120, 50)

        self.chart = self.chartView.chart()
        self.chart.legend().setVisible(False)
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setBackgroundRoundness(0)
        self.chart.setMargins(QtCore.QMargins(3, 3, 3, 3))
        self.chart.setAcceptHoverEvents(True)

        self.combo_type = QtWidgets.QComboBox(self.central_widget)
        self.combo_type.setGeometry(QtCore.QRect(50, 20, 120, 30))

        self.combo_year = QtWidgets.QComboBox(self.central_widget)
        self.combo_year.setGeometry(QtCore.QRect(180, 20, 120, 30))
        self.combo_year.currentIndexChanged.connect(self.combo_year_change)

        self.label_year_distance = QtWidgets.QLabel(self.central_widget)
        self.label_year_distance.setGeometry(600, 60, 100, 50)

        self.label_year_distance_diff = QtWidgets.QLabel(self.central_widget)
        self.label_year_distance_diff.setGeometry(600, 120, 100, 50)

        self.label_year_time = QtWidgets.QLabel(self.central_widget)
        self.label_year_time.setGeometry(600, 180, 100, 50)

        self.label_year_time_diff = QtWidgets.QLabel(self.central_widget)
        self.label_year_time_diff.setGeometry(600, 240, 100, 50)


        stats.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(stats)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        stats.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(stats)
        stats.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(stats)

        self.reset_form()

    def reset_form(self):
        self.get_year_comparison_stats()
        self.get_all_years_stats()
        self.populate_combo_years()
        self.plot_chart()

        self.label_year_distance.setText(str(self.get_total_distance()))
        self.label_year_distance_diff.setText(str(self.get_total_distance_diff()))
        self.label_year_time.setText(str(self.get_total_time()))
        self.label_year_time_diff.setText(str(self.get_total_time_diff()))

    def populate_combo_years(self):
        self.combo_year.clear()
        for year in [x.Year for x in self.year_stats]:
            self.combo_year.addItem(str(year))

    def combo_year_change(self):
        self._current_year = int(self.combo_year.currentText())
        self.get_year_comparison_stats()
        self.plot_chart()

    def get_total_distance(self):
        return dec(self.comparison_stats[self.comparison_stats['year'] == str(self._current_year)]['distance'].max(), 2)

    def get_total_distance_diff(self):
        day = self.comparison_stats[self.comparison_stats['distance'] == float(self.get_total_distance())]['day'].max()
        return self.get_total_distance() - dec(self.comparison_stats[(self.comparison_stats['day'] == day) &
                                                                     (self.comparison_stats['year'] == str(self._current_year - 1))]['distance'].max(), 2)

    def get_total_time(self):
        return dec(self.comparison_stats[self.comparison_stats['year'] == str(self._current_year)]['distance'].max(), 2)

    def get_total_time_diff(self):
        day = self.comparison_stats[self.comparison_stats['distance'] == float(self.get_total_distance())]['day'].max()
        return self.get_total_distance() - dec(self.comparison_stats[(self.comparison_stats['day'] == day) &
                                                                     (self.comparison_stats['year'] == str(self._current_year - 1))]['distance'].max(), 2)

    def tooltip(self, event, series_name):
        pos = self.chart.mapToPosition(event)
        event_date = datetime.datetime.fromtimestamp(event.x() / 1000).strftime('%m-%d')
        event_value = self.comparison_stats[self.comparison_stats['day'] == event_date]
        current_value = event_value[event_value['year'] == str(self._current_year)]['distance']
        current_output = 0 if current_value.empty else current_value.item()
        previous_value = event_value[event_value['year'] == str(self._current_year - 1)]['distance']
        previous_output = 0 if previous_value.empty else previous_value.item()
        self.label_result.setText(f'{event_date}\n{self._current_year}: {current_output}\n{self._current_year - 1}: {previous_output}')
        self.label_result.show()

    def get_year_comparison_stats(self):
        current_year = f'{self._current_year}'
        previous_year = f'{self._current_year - 1}'
        query = sql_queries.year_stats.format(previous=self._current_year - 1,
                                              current=self._current_year,
                                              next=self._current_year + 1)
        stats = pandas.read_sql(query, settings.database.connection, index_col='dayOfYear')
        stats[current_year] = stats['CumCurrentDistance'].astype('float64')
        stats[previous_year] = stats['CumPreviousDistance'].astype('float64')
        stats = stats[[previous_year, current_year]].stack(0)
        self.comparison_stats = stats.reset_index()
        self.comparison_stats.columns = ['day', 'year', 'distance']

    def get_all_years_stats(self):
        self.year_stats = settings.database.get_year_summaries()

    def plot_chart(self):
        label_font = QtGui.QFont()
        label_font.setPixelSize(10)
        axisx = QDateTimeAxis()
        axisx.setFormat("MMM")
        axisx.setTickCount(12)
        axisx.setLabelsFont(label_font)
        axisy = QValueAxis()
        max(self.comparison_stats['distance'].max() + (300 - (self.comparison_stats['distance'].max() % 300)),
            900)
        y_range = max(self.comparison_stats['distance'].max() + (300 - (self.comparison_stats['distance'].max() % 300)),
                      900)
        axisy.setRange(0, y_range)
        axisy.setTickCount((y_range / 300) + 1)
        axisy.setLabelsFont(label_font)
        axisy.setLabelFormat("%.0f")
        self.chart.removeAllSeries()
        for axes in self.chart.axes():
            self.chart.removeAxis(axes)
        self.chart.addAxis(axisx, QtCore.Qt.AlignBottom)
        self.chart.addAxis(axisy, QtCore.Qt.AlignLeft)

        for year in [self._current_year - 1, self._current_year]:
            series = QLineSeries()
            for row in self.comparison_stats[self.comparison_stats['year'] == str(year)].itertuples():
                moment = QtCore.QDateTime().fromString(row.day + f'-{self._current_year}', 'MM-dd-yyyy')
                moment.toMSecsSinceEpoch()
                series.append(moment.toMSecsSinceEpoch(), row.distance)
            self.chartView.chart().addSeries(series)
            series.attachAxis(axisx)
            series.attachAxis(axisy)
            series.hovered.connect(functools.partial(self.tooltip, series_name=str(year)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    stats = QtWidgets.QMainWindow()
    ui = UiStats()
    ui.setup_ui(stats)
    stats.show()
    sys.exit(app.exec_())
