
import sys
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import time
import socket
from threading import Thread

BUFFER_SIZE = 1024 
# laser_keep_scan = True
laser_keep_scan = False

class MainControlWindow(object):
    
    default_wavelength = 620.5
    start_wavelength = 620.6
    end_wavelength = 620.65
    wavelength_step_size = 0.005


    def Check_Work_Done (self, table_connection, confirmation):
        while True:
            try:
                received_msg = table_connection.recv(BUFFER_SIZE).strip() #received the data in binary
            except ConnectionAbortedError as e:
                print(f"Connection was aborted: {e}")
            decoded_received_data = received_msg.decode('utf-8') #change data from binary to string
            if (decoded_received_data == confirmation):
                print("Received from server: ", decoded_received_data)
                break

    def send_message_to_server(self, table_connection, message, confirmation):
        table_connection.sendall(message.encode('utf-8'))
        self.Check_Work_Done(table_connection,confirmation)


    def setupUI(self, main_control_window):
        # main window setup
        main_control_window.setObjectName("main_control_window")
        main_control_window.resize(800,600)
        self.centralwidget = QtWidgets.QWidget(main_control_window)
        main_control_window.setCentralWidget(self.centralwidget)

        # setup DDG label 
        self.DDG_test_label = QtWidgets.QLabel(self.centralwidget)
        self.DDG_test_label.setGeometry(QtCore.QRect(100, 120, 150, 50))
        # setup word features  
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.DDG_test_label.setFont(font)   
        self.DDG_test_label.setAlignment(QtCore.Qt.AlignCenter)
        self.DDG_test_label.setText("DDG")

        # setup DDG button
        self.updateDDG_button = QtWidgets.QPushButton(self.centralwidget)
        self.updateDDG_button.setGeometry(QtCore.QRect(400, 120, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.updateDDG_button.setFont(font)
        self.updateDDG_button.setAutoFillBackground(True)
        self.updateDDG_button.setAutoDefault(True)
        self.updateDDG_button.setFlat(False)
        self.updateDDG_button.setObjectName("udpateDDG_button")
        self.updateDDG_button.setText("OFF")
        
        # setup wavemeter Default label 
        self.wavemeter_default_label = QtWidgets.QLabel(self.centralwidget)
        self.wavemeter_default_label.setGeometry(QtCore.QRect(100, 220, 150, 50))
        # setup word features  
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.wavemeter_default_label.setFont(font)   
        self.wavemeter_default_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wavemeter_default_label.setText("Back to Default")
        self.wavemeter_default_label.adjustSize()

        # setup wavemeter Default button
        self.wavemeter_default_button = QtWidgets.QPushButton(self.centralwidget)
        self.wavemeter_default_button.setGeometry(QtCore.QRect(400, 220, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.wavemeter_default_button.setFont(font)
        self.wavemeter_default_button.setAutoFillBackground(True)
        self.wavemeter_default_button.setAutoDefault(True)
        self.wavemeter_default_button.setFlat(False)
        self.wavemeter_default_button.setObjectName("wavemeter_default_button")
        self.wavemeter_default_button.setText("Default")

        # setup Laser Scan label 
        self.laser_scan_label = QtWidgets.QLabel(self.centralwidget)
        self.laser_scan_label.setGeometry(QtCore.QRect(100, 320, 150, 50))
        # setup word features  
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.laser_scan_label.setFont(font)   
        self.laser_scan_label.setAlignment(QtCore.Qt.AlignCenter)
        self.laser_scan_label.setText("Scan Laser")

        # setup start laser scan button
        self.start_laser_scan_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_laser_scan_button.setGeometry(QtCore.QRect(400, 320, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.start_laser_scan_button.setFont(font)
        self.start_laser_scan_button.setAutoFillBackground(True)
        self.start_laser_scan_button.setAutoDefault(True)
        self.start_laser_scan_button.setFlat(False)
        self.start_laser_scan_button.setObjectName("start_laser_scan_button")
        self.start_laser_scan_button.setText("Start")

        # setup stop laser scan button
        self.stop_laser_scan_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_laser_scan_button.setGeometry(QtCore.QRect(400, 420, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.stop_laser_scan_button.setFont(font)
        self.stop_laser_scan_button.setAutoFillBackground(True)
        self.stop_laser_scan_button.setAutoDefault(True)
        self.stop_laser_scan_button.setFlat(False)
        self.stop_laser_scan_button.setObjectName("stop_laser_scan_button")
        self.stop_laser_scan_button.setText("Stop")


        # button action
        self.updateDDG_button.clicked.connect(self.update_DDGState)
        self.wavemeter_default_button.clicked.connect(self.wavemeter_back_default)
        self.start_laser_scan_button.clicked.connect(self.start_laser_scan)
        self.stop_laser_scan_button.clicked.connect(self.stop_laser_scan)



    def update_DDGState(self):
        if self.updateDDG_button.text() == 'ON': #datatype: str
            self.updateDDG_button.setText("OFF")
            msg_send = "DDG >> end"
            msg_confirmation = "DDG_END"
            self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)
        else:
            self.updateDDG_button.setText("ON")
            # DDG START
            msg_send = "DDG >> start"
            msg_confirmation = "DDG_START"
            self.send_message_to_server(s_table1_linux ,msg_send, msg_confirmation)
         
    def wavemeter_back_default(self):
        # Set Default Wavelength for DYE_LASER
        dye_laser_msg = "DYE_LASER >> setwavelength, " + str(self.default_wavelength)
        msg_confirmation = "DYE_WAVELENGTH_DONE"
        self.send_message_to_server (s_table1_linux, dye_laser_msg, msg_confirmation)
        print(self.default_wavelength)
        self.start_laser_scan_button.setText("Start")


    def Laser_Scan(self):
        global laser_keep_scan
        start_point = self.start_wavelength
        end_point = self.end_wavelength
        step_size = self.wavelength_step_size
        # check whether DDG is "ON"
        if self.updateDDG_button.text() == 'OFF':
                print("Please turn on DDG")
        while start_point <= end_point and laser_keep_scan and self.updateDDG_button.text() == "ON":
            # Set Wavelength for DYE_LASER
            dye_laser_msg = "DYE_LASER >> setwavelength, " + str(start_point)
            msg_confirmation = "DYE_WAVELENGTH_DONE"
            self.send_message_to_server (s_table1_linux, dye_laser_msg, msg_confirmation)
            self.start_laser_scan_button.setText(str(start_point))

            # # Read Wavemeter
            # # ****************************
            # msg_send = "WAVEMETER >> read "
            # msg_confirmation = "TABLE1_DONE"
            # self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)

            # # VIS_SHUTTER ON ("3_on")
            # msg_send = "SHUTTER >> 3_on"
            # msg_confirmation = "VIS_SHUTTER_ON"
            # self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)
            
            # scope to get data
            send_command_scope = "SCOPE >> getData"
            msg_confirmation = "SCOPE_DATA_DONE"
            self.send_message_to_server(s_table1_linux, send_command_scope, msg_confirmation)

            # # VIS_SHUTTER OFF ("3_off")
            # msg_send = "SHUTTER >>3_off"
            # msg_confirmation = "VIS_SHUTTER_OFF"
            # self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)

            # # UV_SHUTTER ON ("4_on")
            # msg_send = "SHUTTER >> 4_on"
            # msg_confirmation = "UV_SHUTTER_ON"
            # self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)

            # # UV_SHUTTER OFF ("4_off")
            # msg_send = "SHUTTER >> 4_off"
            # msg_confirmation = "UV_SHUTTER_OFF"
            # self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)

            # update wavelength
            start_point = start_point + step_size
            print(start_point)
            print(laser_keep_scan)
            # time.sleep(2)
        # if successfully scanned
        if start_point > self.end_wavelength:
            print("******************DONE!**********************")

            # After getting data, let SCOPE come back to normal mode
            scope_back_to_normal = "SCOPE >> BackToNormalMode"
            msg_confirmation =  "SCOPE_NORMAL_MODE"
            self.send_message_to_server(s_table1_linux, scope_back_to_normal, msg_confirmation)

            # turn of DDG 
            msg_send = "DDG >> end"
            msg_confirmation = "DDG_END"
            self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)
            self.updateDDG_button.setText("OFF")
            # change the label text 
            self.start_laser_scan_button.setText("Start")
            print("******************DONE!**********************")

    def start_laser_scan(self):
        global thread_ScanLaser, laser_keep_scan
        laser_keep_scan = True
        thread_ScanLaser = Thread(target = self.Laser_Scan)
        thread_ScanLaser.start()
        
        
    def stop_laser_scan(self):
        # stop laser
        global laser_keep_scan
        laser_keep_scan = False
        # turn off DDG channel 
        msg_send = "DDG >> end"
        msg_confirmation = "DDG_END"
        self.send_message_to_server(s_table1_linux, msg_send, msg_confirmation)
        # change the text of start_laser_scan_button
        self.start_laser_scan_button.setText("Start")
        

if __name__ == "__main__":
    import sys

    # *************************************************************************
    #                Setup & Connection
    # *************************************************************************
    HOST_Table1_LINUX, PORT = "10.246.8.119", 9999
    s_table1_linux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_table1_linux.connect((HOST_Table1_LINUX, PORT))
 
    app = QtWidgets.QApplication(sys.argv)
    main_control_window = QtWidgets.QMainWindow()
    ui = MainControlWindow()
    ui.setupUI(main_control_window)
    main_control_window.show()
    sys.exit(app.exec_())
