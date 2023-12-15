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
from SCOPE_class import *
from DYE_LASER import Dye_Laser
from SHUTTER_class import SHUTTER
from DDG_class import *


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


shutter = SHUTTER()
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
                ddg.DDG_Start(info_dict)
                ddg_response = "DDG_START"
                s_connection.sendall(ddg_response.encode('utf-8'))

            # DDG >> end
            elif (parts[0] == "end"):
                ddg.DDG_End(info_dict)
                ddg_response = "DDG_END"
                s_connection.sendall(ddg_response.encode('utf-8'))

            # "DDG >> 7, delay, -520e-6"                
            else:
                channel = parts[0]
                channel = int(channel)
                # Access the channel instance directly from the channels dictionary
                channel_instance = ddg.channels[channel]

                action = parts[1]
                # Get the method (action)
                method = getattr(channel_instance, f'set_{action}')
               
                value = parts[2]
                # Call the method with value as the argument
                # ddg.channels[1].set_state("ON", ddg.connection, info_dict)
                method(str(value), ddg.connection, info_dict)

                ddg_response = "DDG_DONE"
                s_connection.send(ddg_response.encode('utf-8')) 

        elif (function_name == "SCOPE"):
            parts = function_parameter.split(",")

            # SCOPE >> getData
            if (parts[0] == "getData"):
                print("In function - getData")
                scope.SCOPE_StartToAcquireData()
                print("Done - scope.SCOPE_StartToAcquireData()")
                scope.SCOPE_GetandUpdate_Data(info_dict)
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
            shutter.control_shutter(msg)
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



            
