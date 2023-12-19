# Spectroscopy
Got the spectroscopy data from scanning 

### Client Desktop use GUI
### Table 1 (Linux) - DDG, SCOPE, DYE-LASER, SHUTTER & DATABASE
### Table 2 (Windows) - WAVEMETER

## The Overall Structure
1. We use GUI to talk to "Table 1" only.
2. "Table 1" talks to "Table 2" for any work that needs to be done related to "Table 2"

## Running Process
1. Start the "Table 2" python file (as server) first since it also works as the server for "Table 1"
2. Start the "Table 1" python file (as server)
3. run GUI python file

## In GUI:
When we send messages to the server, we need to confirm the task is done before we send another task. The function to check it is:
def send_message_to_server(self, table_connection, message, confirmation)
In this function, we have "message" which is the msg we send to devices & "confirmation" message as the feedback from the device to confirm that the work has been done!

### *************  
### Arduino:
### *************  
#### Message Examples:
message = "SHUTTER >> 2_on"  
confirmation = "WAVEMETER_SHUTTER_ON"  
message = "SHUTTER >> 2_off"  
confirmation = "WAVEMETER_SHUTTER_OFF"  
message = "SHUTTER >> 3_on"  
confirmation = "VIS_SHUTTER_ON"  
message = "SHUTTER >> 3_off"  
confirmation = "VIS_SHUTTER_OFF"  
message = "SHUTTER >> 4_on"  
confirmation = "UV_SHUTTER_ON"  
message = "SHUTTER >> 4_off"  
confirmation = "UV_SHUTTER_OFF"  

### *************  
### DDG (8 channels):
### *************  
1. set_state(self, state_status, connection, info_dict)  
2. set_delay(self, delay_value, connection, info_dict)  
3. set_sync_channel(self, channel, connection, info_dict)  
4. set_width(self, width_val, connection, info_dict)  
#### Message Examples:
the client sends a message: "DDG >> start"  
server responses message: "DDG_START"  
the client sends a message: "DDG >> end"  
server responses message: "DDG_END"  
the client sends a message: "DDG >> 7, delay, -520e-6" (channel NO., action, value)  
server responses message: "DDG_DONE"  

### Scope (4 channels):
#### Message Examples:
client message: "Scope >> getData"  
server response: "SCOPE_DATA_DONE"  
client message: "Scope >> BackToNormalMode"  
server response: "SCOPE_NORMAL_MODE"  

### Dye Laser:
#### Message Examples:
client message: "DYE_LASER >> setwavelength, 622"  
server response: "DYE_WAVELENGTH_DONE"  
client message: "DYE_LASER >> close"  
server response: "DYE_LASER_CLOSE"  



