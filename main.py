import socket
import sys
import time

BUFFER_SIZE = 1024

def Check_Work_Done (self, table_connection, msg_confirmation):
    while True:
        try:
            received_msg = table_connection.recv(BUFFER_SIZE).strip() #received the data in binary
        except ConnectionAbortedError as e:
            print(f"Connection was aborted: {e}")
        decoded_received_data = received_msg.decode('utf-8') #change data from binary to string
        if (decoded_received_data == msg_confirmation):
            print("Received from server: ", decoded_received_data)
            break

def send_message_to_server(table_connection, message):
    # s_table1_linux.sendall(message.encode('utf-8'))
    table_connection.sendall(message.encode('utf-8'))
    Check_Work_Done(table_connection, message)

# *************************************************************************
#                Setup & Connection
# *************************************************************************
# Create a socket object for TCP/IP connection
# It represents one endpoint of a two-way communication link between the client and server.
s_table1_linux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Host and port of the server we want to connect to
HOST_Table1_LINUX, PORT = "10.246.8.119", 9999
# connect the socket to the server
s_table1_linux.connect((HOST_Table1_LINUX, PORT))

# *************************************************************************
#                Start to Send Messages
# *************************************************************************

# DDG START
msg_send = "DDG >> start"
send_message_to_server(s_table1_linux ,msg_send)

# WAVEMETER_SHUTTER ON ("2_on")
msg_send = "SHUTTER >> 2_on"
send_message_to_server(s_table1_linux, msg_send)


# Start LOOP
wavelength = 620.05
for i in range (30):
    # Set Wavelength for DYE_LASER
    dye_laser_msg = "DYE_LASER >> setwavelength, " + str(wavelength + i * 0.005)
    send_message_to_server (s_table1_linux, dye_laser_msg)

    # Read Wavemeter
    # ****************************
    msg_send = "WAVEMETER >> read "
    send_message_to_server(s_table1_linux, msg_send)
    # ****************************

    # VIS_SHUTTER ON ("3_on")
    msg_send = "SHUTTER >> 3_on"
    send_message_to_server(s_table1_linux, msg_send)
 
    # scope to get data
    send_command_scope = "SCOPE >> getData"
    send_message_to_server(s_table1_linux, send_command_scope)

    # VIS_SHUTTER OFF ("3_off")
    msg_send = "SHUTTER >>3_off"
    send_message_to_server(s_table1_linux, msg_send)

    # UV_SHUTTER ON ("4_on")
    msg_send = "SHUTTER >> 4_on"
    send_message_to_server(s_table1_linux, msg_send)

    # scope to get data
    send_command_scope = "SCOPE >> getData"
    send_message_to_server(s_table1_linux, send_command_scope)

    # UV_SHUTTER OFF ("4_off")
    msg_send = "SHUTTER >> 4_off"
    send_message_to_server(s_table1_linux, msg_send)

# WAVEMETER_SHUTTER OFF ("2_off")
msg_send = "SHUTTER >> 2_off"
send_message_to_server(s_table1_linux, msg_send)

# After getting data, let SCOPE come back to normal mode
scope_back_to_normal = "SCOPE >> BackToNormalMode"
send_message_to_server(s_table1_linux, scope_back_to_normal)

msg_send = "DDG >> end"
send_message_to_server(s_table1_linux, msg_send)

