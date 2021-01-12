from __future__ import annotations
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    '''
    The PyQt5 main window.

    '''

    def __init__(self, username=None):
        super(ApplicationWindow, self).__init__()

        self.username = username

        # 1. Window settings
        self.setGeometry(300, 300, 800, 480)
        self.setWindowTitle("ECG")
        # self.setWindowTitle("Matplotlib live plot in PyQt - example 2")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QtWidgets.QVBoxLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

        # self.backButton = QtWidgets.QPushButton('BACK', self)
        # self.backButton.resize(100, 32)
        # self.backButton.move(610, 25)

        # self.backButton.clicked.connect(self.backButtonClicked)

        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=20)
        self.lyt.addWidget(self.myFig)

        # 3. Show
        self.show()
        return

    # def backButtonClicked(self):
    #
    #     self.close()

    def closeEvent(self, event):

        print("Graph closed.")
        event.accept()


class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self, x_len: int, y_range: List, interval: int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_,
                                    fargs=(y,), interval=interval, blit=True)

        self.openECGPort()

        return

    def openECGPort(self):
        # self.ecgPort = serial.Serial(port=ecgPortName, baudrate=9600)
        self.ecgDataList = []

    def closeECGPort(self):
        if self.ecgPort.isOpen():
            self.ecgPort.close()

    def readECGPort(self):
        self.ecgReading = 60
        self.ecgDataList.append(1)

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''

        self.readECGPort()

        # time.sleep(1)

        y.append(round(self.ecgReading, 2))     # Add new datapoint
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)

        return self._line_,


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ApplicationWindow()
    w.show()
    app.exec_()
else:
    app = QtWidgets.QApplication(sys.argv)
    w = ApplicationWindow()
    w.show()
    app.exec_()
