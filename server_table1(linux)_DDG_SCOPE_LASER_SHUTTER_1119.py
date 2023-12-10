import socket
import serial
import time
#from vimba import *
import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from logging import info
import vxi11
import pickle
from datetime import datetime
from wlm import *


BUFFER_SIZE = 1024
info_dict = {}

def Command_parse_run(command):
    # parse input parameters
    command = command.replace(" ", "")
    if (command.find('>>')!=-1):
        command_func_name = command.split('>>')[0]
        command_func_parameter = command.split('>>')[1]
    else:
        command_func_name = None
        command_func_parameter = None
    return command_func_name, command_func_parameter

def Check_Work_Done (table_connection, confirmation):
    while True:
        received_msg = table_connection.recv(BUFFER_SIZE).strip() #received the data in binary
        decoded_received_data = received_msg.decode('utf-8') #change data from binary to string
        if (decoded_received_data == confirmation):
            print("Received from server: ", decoded_received_data)
            break

def send_message_to_server(table_connection, message, confirmation):
    # s_table1_linux.sendall(message.encode('utf-8'))
    table_connection.sendall(message.encode('utf-8'))
    Check_Work_Done(table_connection,confirmation)

def Shutter_Control (msg):
    shutter.write(str.encode(msg))
    # line = shutter.readline()
    line = shutter.read_until()
    # line = line.decode().strip('\r\n')
    # print(line)


# class WAVEMETER:
#     wavemeter = serial.Serial('COM3', 115200)
#     time.sleep(0.1)
#     wavemeter.write(b'I1 1\r\n')

#     def Read_Wavemeter (self):
#         print("In function - Read Wavemeter")
#         wlm = WavelengthMeter()
#         current_wavelength = float(wlm.wavelength)
#         print (current_wavelength)

class Dye_Laser:
    HOST_DYE = '10.246.8.124'
    PORT_DYE = 65510
    laser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    laser.connect((HOST_DYE, PORT_DYE))

    def __init__(self):
        print("start to create dye laser")
        # HOST_DYE = '10.246.8.124'
        # PORT_DYE = 65510
        # self.laser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.laser.connect((HOST_DYE, PORT_DYE))
        self.BUFFER_SIZE = 1024
        self.remote_connection()
        # print("Create Dye Laser")

    def remote_connection(self):
        remote_connect_msg = "RemoteConnect\r\n"
        self.laser.send(remote_connect_msg.encode('utf-8'))
        data = self.laser.recv(self.BUFFER_SIZE)
        print(data.decode('utf-8'))

    def set_wavelength(self, wavelength):
        msg = "SetWavelength " + str(wavelength) + "\r\n"
        self.laser.send(msg.encode('utf-8')) #convert the string to bytes
        info_dict["Dye_Laser_wavelength"] = wavelength
        data = self.laser.recv(self.BUFFER_SIZE)
        print(data.decode('utf-8'))

    def close_laser(self):
        self.laser.close()



class DDG_channel_1:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_1.state"] = state_status
        # msg = ":PULSE1:STAT ON\r\n"
        msg = ":PULSE1:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_1.delay"] = delay_value
        # msg = ":PULSE1:DEL -135e-6\r\n"
        msg = ":PULSE1:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_1.sync_channel"] = channel
        # msg = ":PULSE1:SYNC CHB\r\n"
        msg = ":PULSE1:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_1.width"] = width_val
        # msg = ":PULSE1:WIDT 10e-6\r\n"
        msg = ":PULSE1:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_2:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_2.state"] = state_status
        msg = ":PULSE2:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_2.delay"] = delay_value
        msg = ":PULSE2:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_2.sync_channel"] = channel
        msg = ":PULSE2:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_2.width"] = width_val
        msg = ":PULSE2:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_3:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_3.state"] = state_status
        msg = ":PULSE3:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_3.delay"] = delay_value
        msg = ":PULSE3:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_3.sync_channel"] = channel
        msg = ":PULSE3:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_3.width"] = width_val
        msg = ":PULSE3:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_4:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_4.state"] = state_status
        msg = ":PULSE4:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_4.delay"] = delay_value
        msg = ":PULSE4:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_4.sync_channel"] = channel
        msg = ":PULSE4:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_4.width"] = width_val
        msg = ":PULSE4:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_5:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_5.state"] = state_status
        msg = ":PULSE5:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_5.delay"] = delay_value
        msg = ":PULSE5:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_5.sync_channel"] = channel
        msg = ":PULSE5:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_5.width"] = width_val
        msg = ":PULSE5:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_6:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_6.state"] = state_status
        msg = ":PULSE6:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_6.delay"] = delay_value
        msg = ":PULSE6:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_6.sync_channel"] = channel
        msg = ":PULSE6:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_6.width"] = width_val
        msg = ":PULSE6:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_7:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_7.state"] = state_status
        msg = ":PULSE7:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_7.delay"] = delay_value
        msg = ":PULSE7:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_7.sync_channel"] = channel
        msg = ":PULSE7:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_7.width"] = width_val
        msg = ":PULSE7:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG_channel_8:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["DDG_channel_8.state"] = state_status
        msg = ":PULSE8:STAT " + state_status + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_delay (self, delay_value):
        self.delay = delay_value
        info_dict["DDG_channel_8.delay"] = delay_value
        msg = ":PULSE8:DEL " + delay_value + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_sync_channel (self, channel):
        self.sync_channel = channel
        info_dict["DDG_channel_8.sync_channel"] = channel
        msg = ":PULSE8:SYNC " + channel + "\r\n"
        DDG.connection.write(str.encode(msg))        
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

    def set_width (self, width_val):
        self.width = width_val
        info_dict["DDG_channel_8.width"] = width_val
        msg = ":PULSE8:WIDT " + width_val + "\r\n"
        DDG.connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        DDG.connection.readline()

class DDG:
    connection = serial.Serial('/dev/ttyUSB0', 115200)
    def __init__(self):
        self.DDG_channel_1 = DDG_channel_1()
        self.DDG_channel_2 = DDG_channel_2()
        self.DDG_channel_3 = DDG_channel_3()
        self.DDG_channel_4 = DDG_channel_4()
        self.DDG_channel_5 = DDG_channel_5()
        self.DDG_channel_6 = DDG_channel_6()
        self.DDG_channel_7 = DDG_channel_7()
        self.DDG_channel_8 = DDG_channel_8()
        self.DDG_Initialization()
    
    # channel 1 & 2 ON
    # channel 3 & 5 & 6 & 7 & 8 OFF
    # channel 4(D) - nothing 
    def DDG_Initialization(self):
        # Declare the dictionary as global, not create a new local one
        global info_dict 
        # ****************************************************************
        # channel A - Nd: YAG flashlamp
        # state on
        self.DDG_channel_1.set_state("ON")
        # channel A SYNC channel B   
        self.DDG_channel_1.set_sync_channel("CHB")
        # set channel A delay: -135e-6 (-135um)    
        self.DDG_channel_1.set_delay("-135e-6")
        # set channel A width to 10e-6    
        self.DDG_channel_1.set_width("10e-6")
        # ****************************************************************
        # channel B - Nd: YAG Q-switch
        # state on
        self.DDG_channel_2.set_state("ON")
        # channel B SYNC channel F
        self.DDG_channel_2.set_sync_channel("CHF")
        # set channel B delay: 470e-6 
        self.DDG_channel_2.set_delay("470e-6")
        # set channel B width to 10e-6
        self.DDG_channel_2.set_width("10e-6")
        # ****************************************************************
        # channel C - Scope trigger
        # state on
        self.DDG_channel_3.set_state("OFF")
        # channel C SYNC channel B
        self.DDG_channel_3.set_sync_channel("CHB")
        # set channel C delay: 0
        self.DDG_channel_3.set_delay("0")
        # set channel C width to 10e-6
        self.DDG_channel_3.set_width("10e-6")
        # ****************************************************************
        # channel D - NOTHING RIGHT NOW
        # state on
        self.DDG_channel_4.set_state("OFF")
        # channel C SYNC channel B
        self.DDG_channel_4.set_sync_channel("CHB")
        # set channel C delay: 0
        self.DDG_channel_4.set_delay("0")
        # set channel C width to 10e-6
        self.DDG_channel_4.set_width("10e-6")
        # ****************************************************************
        # channel E - ablation flashlamp
        # state off
        self.DDG_channel_5.set_state("OFF")
        # channel E SYNC channel T0
        self.DDG_channel_5.set_sync_channel("T0")
        # set channel E delay: 10e-3 
        self.DDG_channel_5.set_delay("10e-3")
        # set channel E width to 10e-6
        self.DDG_channel_5.set_width("10e-6")
        # ****************************************************************
        # channel F - ablation Q-switch
        # state off
        self.DDG_channel_6.set_state("OFF")
        # channel F SYNC channel E
        self.DDG_channel_6.set_sync_channel("CHE")
        # set channel F delay: 110e-6 
        self.DDG_channel_6.set_delay("110e-6")
        # set channel F width to 10e-6
        self.DDG_channel_6.set_width("10e-6")
        # ****************************************************************
        # channel G - nozzle
        # state oFF
        self.DDG_channel_7.set_state("OFF")
        self.DDG_channel_7.set_sync_channel("CHF")
        self.DDG_channel_7.set_delay("-460e-6")
        self.DDG_channel_7.set_width("250e-6")
        # ****************************************************************
        # channel H - PMT switch
        self.DDG_channel_8.set_state("OFF")
        self.DDG_channel_8.set_sync_channel("CHB")
        self.DDG_channel_8.set_delay("-680e-9")
        self.DDG_channel_8.set_width("1e-6")

    # All channel ON 
    def DDG_Start(self):
        self.DDG_channel_3.set_state("ON")
        self.DDG_channel_5.set_state("ON")
        self.DDG_channel_6.set_state("ON")
        self.DDG_channel_7.set_state("ON")
        self.DDG_channel_8.set_state("ON")

    # channel 1 & 2 ON
    # channel 3 & 5 & 6 & 7 & 8 OFF
    def DDG_End(self):
        self.DDG_channel_3.set_state("OFF")
        self.DDG_channel_5.set_state("OFF")
        self.DDG_channel_6.set_state("OFF")
        self.DDG_channel_7.set_state("OFF")
        self.DDG_channel_8.set_state("OFF")

class SCOPE_channel_1:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["SCOPE_channel_1.state"] = state_status
        msg = "SELect:CH1 " + state_status
        SCOPE.connection.write(msg)

class SCOPE_channel_2:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["SCOPE_channel_2.state"] = state_status
        msg = "SELect:CH2 " + state_status
        SCOPE.connection.write(msg)

class SCOPE_channel_3:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["SCOPE_channel_3.state"] = state_status
        msg = "SELect:CH3 " + state_status
        SCOPE.connection.write(msg)

class SCOPE_channel_4:
    def set_state (self, state_status):
        self.state = state_status
        info_dict["SCOPE_channel_4.state"] = state_status
        msg = "SELect:CH4 " + state_status
        SCOPE.connection.write(msg)

class SCOPE:
    connection = vxi11.Instrument("10.246.8.106")
    def __init__(self):
        self.SCOPE_channel_1 = SCOPE_channel_1()
        self.SCOPE_channel_2 = SCOPE_channel_2()
        self.SCOPE_channel_3 = SCOPE_channel_3()
        self.SCOPE_channel_4 = SCOPE_channel_4()
        self.SCOPE_Initialization()

    def SCOPE_Initialization(self):
        points = 5000
        self.connection.write("HORizontal:MAIn:SCAle 200e-9")
        self.connection.write("DATa:ENCdg ASCii") # Set the data format, ASCII here 
        self.connection.write("WFMOutpre:BYT_Nr 1") 
        self.connection.write("DATa:STARt 1") # data start point, first position is 1 
        self.connection.write("DATa:STOP {}".format(points)) # data end point 
        self.connection.write("DATa:SOUrce CH3") # pick up channel
        self.connection.write("ACQuire:STOPAfter SEQuence") 
      
        # channel 2 & 3 ON
        # channel 1 & 4 OFF
        self.SCOPE_channel_1.set_state("OFF")
        self.SCOPE_channel_2.set_state("ON")
        self.SCOPE_channel_3.set_state("ON")
        self.SCOPE_channel_4.set_state("OFF")

    def SCOPE_StartToAcquireData(self):
        self.connection.write("HORizontal:FASTframe:STATE ON")
        self.connection.write("HORizontal:FASTframe:COUNt 20")
        self.connection.write("ACQuire:STATE RUN") # when acquiring data: STATE == 1

    def SCOPE_GetandUpdate_Data(self):
        # when acquiring data process is DOEN, STATE == 0
        need_state = ":ACQUIRE:STATE 1" 
        test_state = self.connection.ask("ACQuire:STATE?")
        while(test_state == need_state):
            test_state = self.connection.ask("ACQuire:STATE?")
            time.sleep(0.1)
        self.raw_data = self.connection.ask("CURVe?") # transfer data to us
        
        #update the raw_data
        data_arr = self.raw_data.split()
        data_arr.pop(0) #take off "curve:"
        data_str = data_arr[0] #datatype is string
        data_list = data_str.split(',') #splite str based on ','
        data_float_list = [float(i) for i in data_list]
        #get X_zero - XZE_num
        XZE = self.connection.ask("WFMO:XZE?")
        XZE_arr = XZE.split()
        XZE_num = float(XZE_arr[1])
        # print("XZE_num is: ", XZE_num)
        #get x increase step - XIN_num
        XIN = self.connection.ask("WFMO:XIN?")
        XIN_arr = XIN.split()
        XIN_num = float(XIN_arr[1])
        # print("X increase step is: ", XIN_num)
        #get y off value - YOF_num
        YOF = self.connection.ask("WFMO:YOF?") 
        YOF_arr = YOF.split()
        YOF_num = float(YOF_arr[1])
        # print("Y off amount is: ", YOF_num)
        #get y multiplier - YMU_num
        YMU = self.connection.ask("WFMO:YMU?") 
        YMU_arr = YMU.split()
        YMU_num = float(YMU_arr[1])
        # print("Y off amount is: ", YMU_num)
        #get y zero point - YZE_num
        YZE = self.connection.ask("WFMO:YZE?")
        YZE_arr = YZE.split()
        YZE_num = float(YZE_arr[1])
        #Calculation formula: 
        # y = (data-YOF_num)*YMU_num + YZE_num
        # x = 0 + XIN_num * i
        self.updated_scope_data = []
        for i in data_float_list:
            self.updated_scope_data.append((i-YOF_num)*YMU_num+YZE_num)

        # size = len(self.updated_scope_data)
        # print(size)

        # updated_x = []
        # for i in range(size):
        #     updated_x.append(i*XIN_num)
        #print(update_x)
        # write to dictionary    
        info_dict["scope.data"] = self.updated_scope_data

    def SCOPE_BackToNormalMode(self):
        self.connection.write("HORizontal:FASTframe:STATE OFF") # get the scope back to the normal mode

def create_folder (base_path, prefix):
    # Get today's date in MMDD format
    date_str = datetime.now().strftime('%m%d')
    # Initialize folder number
    folder_num = 1
    # Construct folder name and path
    folder_name = f"{prefix}_{date_str}_v{folder_num}"
    folder_path = os.path.join(base_path, folder_name)
    # Check if the folder exists, if it does, create new one with an incremented suffix
    while os.path.exists(folder_path):
        folder_num += 1
        folder_name = f"{prefix}_{date_str}_v{folder_num}"
        folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    print(f'Created folder: {folder_path}')
    return folder_path

def create_file (folder_path):
    # Define file prefix and extension
    file_prefix = 'file_'
    extension = '.pkl'
    # Initialize file number
    file_num = 1
    # Construct new file path
    new_file_path = os.path.join(folder_path, f"{file_prefix}{file_num}{extension}")    
    # Check if the file exists, if it does, create new one with an incremented suffix
    while os.path.isfile(new_file_path):
        file_num += 1
        new_file_path = os.path.join(folder_path, f"{file_prefix}{file_num}{extension}")
    
    filename = f"{file_prefix}{file_num}{extension}"
    info_dict["filename"] = filename
    # Create a new file
    open(new_file_path, 'a').close()
    print(f'Created file: {new_file_path}')
    return new_file_path

def write_dict_to_file (file_path, dictionary):
    with open(file_path, 'wb') as f:
        pickle.dump(dictionary, f)



# *************************************************************************
#                Setup & Connection
# *************************************************************************

# **************Works as Server***************
# Connect to the Client Desktop as the server
HOST = "10.246.8.119"
PORT = 9999
# Create a new socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binds the socket to the given host and port
s.bind((HOST, PORT))
# Put the server into listening mode. It's now waiting for incoming connections.
s.listen()
print("Server is listening...")
# **************Works as Server***************


# **************Works as Client***************
# Connect to the Table 2 as the client
HOST_Table2_WINDOWS, PORT_2 = "10.246.8.124", 9999
s_table2_windows = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s_table2_windows.connect((HOST_Table2_WINDOWS, PORT_2))
# **************Works as Client***************


shutter = serial.Serial('/dev/Shutter_UNO', 115200, timeout=10)
ddg = DDG() # digital_delay_generator
scope = SCOPE()
dye_laser = Dye_Laser()
# wavemeter = WAVEMETER()
time.sleep(3)

folder_num = 0
while True:
    s_connection, s_address = s.accept()
    #s_table2_windows.connect((HOST_Table2_WINDOWS, PORT))
    print("************connection*******************")
    # folder_path = create_folder("/mnt/my_smb_share", "dataset") 
    folder_path = create_folder("/home/zhoulabspec/smb_mount/Spectra", "dataset") 
    while True:
        # data = s_connection.recv(BUFFER_SIZE)
        # received_command = s_connection.recv(BUFFER_SIZE).strip()
        received_command = s_connection.recv(BUFFER_SIZE)
        if not received_command:
            break
        decoded_received_command = received_command.decode('utf-8') #change to string
        print(decoded_received_command)
        
        function_name, function_parameter = Command_parse_run(decoded_received_command)
        
        if (function_name == "DDG"):
            parts = function_parameter.split(",")

            # DDG >> start
            if (parts[0] == "start"): 
                ddg.DDG_Start()
                ddg_response = "DDG_START"
                s_connection.sendall(ddg_response.encode('utf-8'))

            # DDG >> end
            elif (parts[0] == "end"):
                ddg.DDG_End()
                ddg_response = "DDG_END"
                s_connection.sendall(ddg_response.encode('utf-8'))

            # "DDG >> channel_7, delay, -520e-6"
            else:
                channel = parts[0]
                # print(f"DDG_{channel}")
                channel_instance = getattr(ddg, f'DDG_{channel}')
                action = parts[1]
                # Get the method (action)
                method = getattr(channel_instance, f'set_{action}')
                value = parts[2]
                # Call the method with value as the argument
                method(str(value))
                ddg_response = "DDG_DONE"
                s_connection.send(ddg_response.encode('utf-8')) 

        elif (function_name == "SCOPE"):
            parts = function_parameter.split(",")

            # SCOPE >> getData
            if (parts[0] == "getData"):
                print("In function - getData")
                scope.SCOPE_StartToAcquireData()
                print("Done - scope.SCOPE_StartToAcquireData()")
                scope.SCOPE_GetandUpdate_Data()
                print ("Done - scope.SCOPE_GetandUpdate_Data()")
                file_path = create_file(folder_path)
                write_dict_to_file(file_path, info_dict)
                scope_response = "SCOPE_DATA_DONE"
                s_connection.send(scope_response.encode('utf-8')) 

            # Scope >> BackToNormalMode
            if (parts[0] =="BackToNormalMode"):
                scope.SCOPE_BackToNormalMode()
                scope_response = "SCOPE_NORMAL_MODE"
                s_connection.send(scope_response.encode('utf-8')) 

        elif (function_name == "DYE_LASER"):
            parts = function_parameter.split(',')

            # DYE_LASER >> setwavelength, 622
            if (parts[0] == "setwavelength"):
                dye_laser.set_wavelength(parts[1])
                dye_laser_response = "DYE_WAVELENGTH_DONE"
                s_connection.send(dye_laser_response.encode('utf-8'))

            # DYE_LASER >> close
            elif (parts[0] == "close"):
                dye_laser.close_laser()
                dye_laser_response = "DYE_LASER_CLOSE"
                s_connection.send(dye_laser_response.encode('utf-8'))

        elif (function_name == "SHUTTER"):
            msg = str(function_parameter)
            Shutter_Control(msg)
            if (msg == "2_on"):
                shutter_response = "WAVEMETER_SHUTTER_ON"
                s_connection.send(shutter_response.encode('utf-8'))
            elif (msg == "2_off"):
                shutter_response = "WAVEMETER_SHUTTER_OFF"
                s_connection.send(shutter_response.encode('utf-8'))
            elif (msg == "3_on"):
                shutter_response = "VIS_SHUTTER_ON"
                s_connection.send(shutter_response.encode('utf-8'))               
            elif (msg == "3_off"):
                shutter_response = "VIS_SHUTTER_OFF"
                s_connection.send(shutter_response.encode('utf-8'))  
            elif (msg == "4_on"):
                shutter_response = "UV_SHUTTER_ON"
                s_connection.send(shutter_response.encode('utf-8'))               
            elif (msg == "4_off"):
                shutter_response = "UV_SHUTTER_OFF"
                s_connection.send(shutter_response.encode('utf-8'))  

        elif (function_name == "WAVEMETER"):
            #send info to table 2 windows to read the wavelength
            print("For wavemeter - Table1 received message from Client")
            s_table2_windows.sendall(received_command)
            
            #receive the wavelength value from table 2
            received_wavelength = s_table2_windows.recv(BUFFER_SIZE).strip()
            info_dict["wavelength_in_wavemeter"] = received_wavelength
            
            #tell client that wavemeter part is done
            msg_send_client = "TABLE1_DONE"
            s_connection.send(msg_send_client.encode('utf-8')) 



            
