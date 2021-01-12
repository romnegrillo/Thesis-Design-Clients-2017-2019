import Front
import Image
import Impedance
from PyQt5 import QtWidgets
import sys

class FrontWindow(QtWidgets.QMainWindow, Front.Ui_MainWindow):

    def __init__(self):
        super(FrontWindow,self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.openImageWindow)
        self.pushButton_2.clicked.connect(self.openImpedanceWindow)

    def openImageWindow(self):
        self.imageWindow=ImageWindow()
        self.hide()
        self.imageWindow.show()

    def openImpedanceWindow(self):
        self.impedanceWindow = ImpedanceWindow()
        self.hide()
        self.impedanceWindow.show()


class ImageWindow(QtWidgets.QMainWindow, Image.Ui_MainWindow):

    def __init__(self):
        super(ImageWindow,self).__init__()
        self.setupUi(self)

class ImpedanceWindow(QtWidgets.QMainWindow, Impedance.Ui_MainWindow):

    def __init__(self):
        super(ImpedanceWindow,self).__init__()
        self.setupUi(self)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = FrontWindow()
    w.show()
    sys.exit(app.exec_())

