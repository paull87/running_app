from PyQt5 import QtCore, QtWidgets
from settings.settings import Settings
import settings.sql_queries as sql_queries
import datetime
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn
import matplotlib
from matplotlib import pyplot
import pandas
import numpy


settings = Settings()


class PlotCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(tight_layout=True)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.axis('off')
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = PlotCanvas()                 # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.setSpacing(0)
        print(self.contentsMargins().top())
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)



matplotlib.use('QT5Agg')
# seaborn.set_style('white', {
#     'axes.spines.bottom': False,
#     'axes.spines.left': False,
#     'axes.spines.right': False,
#     'axes.spines.textop': False})

seaborn.set()
seaborn.set_style("whitegrid")#, {'axes.grid' : False})


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

        self.canvas_years_distance = PlotWidget(self.central_widget)
        self.canvas_years_distance.setGeometry(QtCore.QRect(100, 100, 400, 400))

        #self.canvas_years_time = PlotWidget(self.central_widget)
        #self.canvas_years_time.setGeometry(QtCore.QRect(400, 100, 300, 300))

        stats.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(stats)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        stats.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(stats)
        stats.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(stats)

        self.plot_years_distance()
        #self.plot_years_time()

    def set_current_year_stats(self):
        pass

    def plot_years_distance(self):
        stats = pandas.read_sql(sql_queries.year_stats, settings.database.connection, index_col='dayOfYear')
        stats['Current'] = stats['CumCurrentDistance'].astype('float64')
        stats['Previous'] = stats['CumPreviousDistance'].astype('float64')
        stats = stats[['Previous', 'Current']].stack(0)
        stats = stats.reset_index()
        stats.columns = ['day', 'year', 'distance']
        #self.canvas_years_distance.canvas.ax.get_yaxis().set_visible(False)
        self.canvas_years_distance.canvas.ax.get_xaxis().set_visible(False)
        self.canvas_years_distance.canvas.ax.yaxis.set_minor_locator(pyplot.MultipleLocator(200))
        self.canvas_years_distance.canvas.ax.yaxis.grid(True)
        self.canvas_years_distance.canvas.ax.set_yticklabels([])
        self.canvas_years_distance.canvas.ax.clear()
        self.canvas_years_distance.setHidden(False)
        seaborn.lineplot(x='day', y='distance', data=stats, color='b', hue='year',
                        ax=self.canvas_years_distance.canvas.ax, legend=False)
        self.canvas_years_distance.canvas.draw()

    def plot_years_time(self):
        stats = pandas.read_sql(sql_queries.year_stats, settings.database.connection, index_col='dayOfYear')
        stats['Current'] = stats['CumCurrentTime'].astype('float64')
        stats['Previous'] = stats['CumPreviousTime'].astype('float64')
        stats = stats[['Previous', 'Current']].stack(0)
        stats = stats.reset_index()
        stats.columns = ['day', 'year', 'distance']

        # self.canvas_years_distance.canvas.ax.get_yaxis().set_visible(False)
        self.canvas_years_time.canvas.ax.get_xaxis().set_visible(False)
        self.canvas_years_time.canvas.ax.yaxis.set_minor_locator(pyplot.MultipleLocator(200))
        self.canvas_years_time.canvas.ax.yaxis.grid(True)
        self.canvas_years_time.canvas.ax.set_yticklabels([])
        self.canvas_years_time.canvas.ax.clear()
        self.canvas_years_time.setHidden(False)
        seaborn.lineplot(x='day', y='distance', data=stats, color='b', hue='year',
                        ax=self.canvas_years_time.canvas.ax, legend=False)
        self.canvas_years_time.canvas.draw()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    stats = QtWidgets.QMainWindow()
    ui = UiStats()
    ui.setup_ui(stats)
    stats.show()
    sys.exit(app.exec_())