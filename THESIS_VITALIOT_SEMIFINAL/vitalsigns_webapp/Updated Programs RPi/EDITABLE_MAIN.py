from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.uic import loadUi
import sys

inRPi = True

try:
    import RPi.GPIO
except ImportError:
    inRPi = False
    
class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main,self).__init__()
        loadUi("vitalsigns_main.ui", self)

        self.doctorAssessmentTextbox.setText("Test")
        self.deviceCoordinates.setText("")
        self.bodyTempTB.setText("")
        self.heartRateTB.setText("")
        self.bpStatusTB.setText("")

        # Resp rate to, di ko lang nabago text name.
        self.label_29.setText("")
        self.diastolicTB.setText("")
        self.systolicTB.setText("")

        self.nameTB.setText("")
        self.locationTB.setText("")
        self.sexTB.setText("")
        self.ageTB.setText("")
    
     
        if inRPi:
            self.showFullScreen()

app = QtWidgets.QApplication(sys.argv)
w = Main()
w.show()
app.exec_()
        
