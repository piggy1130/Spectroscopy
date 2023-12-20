import socket
import serial
import time
from wlm import *
from datetime import datetime
import os
#import numpy as np
import pickle
from wavemeter_class import WAVEMETER

BUFFER_SIZE = 1024
info_dict = {}

# def Work_Done():
#     Done_response = "Table2_windows_DONE"
#     client_socket.send(Done_response.encode('utf-8'))


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
    


# *************************************************************************
#                Setup & Connection
# *************************************************************************
HOST_Table2_Windows, PORT = "10.246.8.124", 9999 #SERVER IP address
# Create a TCP/IP socket
s_table2_windows = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific host and port
s_table2_windows.bind((HOST_Table2_Windows, PORT))
# Listen for incoming connections
s_table2_windows.listen(1) #1 means allow 1 connection to wait in queue before processing
print("Server is listening...")

# setup wavemeter
wavemeter = WAVEMETER()

folder_num = 0

while True:
    s_table2_connection, s_table2_address = s_table2_windows.accept()
    print("************connection*******************")
    # folder_path = create_folder("\\\zhoulab-nas-1\Data\Spectra", "wavemeter") 
    while True:
        received_command = s_table2_connection.recv(BUFFER_SIZE)
        if not received_command:
            break
        decoded_received_command = received_command.decode('utf-8') #change to string
        print(decoded_received_command)
        
        function_name, function_parameter = Command_parse_run(decoded_received_command)
        
        if (function_name == "WAVEMETER"):
            parts = function_parameter.split(",")

            # WAVEMETER >> read
            if (parts[0] == "read"): 
                #send wavelength to table1
                wavelength_value = wavemeter.Read_Wavemeter()
                # wavemeter_response = "WAVEMETER_READ_DONE"
                s_table2_connection.sendall(wavelength_value.encode('utf-8'))        

                # s_table2_connection.sendall(wavelength_value.encode('utf-8'))


