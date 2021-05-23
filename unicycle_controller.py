from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from python_qt_binding import loadUi

import serial
import sys

class My_App(QtWidgets.QMainWindow):

    def __init__(self):

        # Intialize User Interface (loaded from the .ui file)
        super(My_App, self).__init__()
        loadUi("./unicycle_controller.ui", self)

        # Setup BT connection
        bt_port = "COM5"
        bt_baud = 9600
        self.log_msg("Attempting bluetooth connection (port: {}; baud: {}".
                format(bt_port, bt_baud)) 
        self.bluetooth = serial.Serial(bt_port, bt_baud)
        ret = bluetooth.flushInput()
        self.log_msg("Bluetooth connected: " + str(ret))
        
        # Connect buttons to functions (SLOTS)
        self.Update_PID_QPB.clicked.connect(self.SLOT_update_PID)
        self.Revert_PID_QPB.clicked.connect(self.SLOT_revert_PID)
        self.Forward_QPB.clicked.connect(self.SLOT_move_forward)

    def SLOT_update_PID(self):
        # Save the PID from the 3 spin boxes
        P = self.PHIKP_QDSB.Value()
        I = self.PHIKI_QDSB.Value()
        D = self.PHIKD_QDSB.Value()
        # Send the PID over serial BT
        self.bluetooth.write(bytes("<P,{}><I,{}><D,{}>".format(P,I,D),'utf-8'))
        # Log the sent data
        self.log_msg("Set PID to P:{}, I: {}, D: {}.".format(P,I,D))
        return


    def SLOT_revert_PID(self):
        self.log_msg("Function not implemented.")
        return


    def SLOT_move_forward(self):
        X_travel = self.XTRAVEL_QDSB.Value()
        self.bluetooth.write(bytes("<F,{}>".format(X_travel), 'utf-8'))
        self.log_msg("Moving forward: {}".format(X_travel))
        return

    def log_msg(self, message):
        now = datetime.now()
        date_time = now.strftime("%H:%M:%S.%f")[:-3]
        log_output = "<font color='blue'>{}</font>: {}".format(date_time, message)
        self.Log_QTE.append(log_output)

        # Save log to file - disabled for now:
        #log_file_content = self.Log_QTE.toPlainText()
        #with open(self.log_file_path, "w") as html_file:
        #    html_file.write(log_file_content)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myApp = My_App()
    myApp.show()
    sys.exit(app.exec_())

