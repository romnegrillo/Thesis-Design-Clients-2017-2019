from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
import sys
import imageprocessing


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        loadUi("classify_window.ui", self)
        self.setFixedSize(self.size())
        self.initGui()

    def initGui(self):
        self.mode = ["Top View", "Side View"]
        self.comboBox.addItems(self.mode)
        self.browseButton.clicked.connect(self.browseButtonClicked)
        self.imgObj = imageprocessing.TrainingImageProcessing()

    def browseButtonClicked(self):
        print("Browse button clicked.")

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Single File', QtCore.QDir.currentPath(), '*.jpg')

        print(fileName)

        try:
            image = self.imgObj.getImage(fileName)

            if(len(image.shape) == 2):
                # One channel.
                imageFormat = QtGui.QImage.Format_Indexed8
            else:
                # Check if three or four channels.
                numChannel = image.shape[2]

                if numChannel == 3:
                    imageFormat = QtGui.QImage.Format_RGB888
                elif numChannel == 4:
                    imageFormat = QtGui.QImage.Format_RGBA8888

            outImage = QtGui.QImage(image, image.shape[1], image.shape[0], image.strides[0],
                                    imageFormat)

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.imageLabel.setScaledContents(True)

            mode = str(self.comboBox.currentText())

            print(mode)

            if mode == self.mode[0]:
                print("Top mode selected.")
            elif mode == self.mode[1]:
                print("Side mode selected.")

            totalArea = self.imgObj.getTotalArea()
            maxima = self.imgObj.getMaximaEllipse()
            minima = self.imgObj.getMinimaEllipse()

        except Exception as exp:
            print(str(exp))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
