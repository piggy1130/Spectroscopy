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

### **************************  
### Arduino:
### **************************  
#### Message Examples:
message = "SHUTTER >> 2_on"  
message = "SHUTTER >> 2_off"  
message = "SHUTTER >> 3_on"  
message = "SHUTTER >> 3_off"  
message = "SHUTTER >> 4_on"  
message = "SHUTTER >> 4_off"  
 

### **************************  
### DDG (8 channels):
### **************************  
1. set_state(self, state_status, connection, info_dict)  
2. set_delay(self, delay_value, connection, info_dict)  
3. set_sync_channel(self, channel, connection, info_dict)  
4. set_width(self, width_val, connection, info_dict)  
#### Message Examples:
the client sends a message: "DDG >> start"  
the client sends a message: "DDG >> end"  
the client sends a message: "DDG >> 7, delay, -520e-6" (channel NO., action, value)  


### **************************  
### Scope (4 channels):
### **************************  
#### Message Examples:
client message: "Scope >> getData"  
client message: "Scope >> BackToNormalMode"  


### **************************  
### Dye Laser:
### **************************  
#### Message Examples:  
client message: "DYE_LASER >> setwavelength, 622"    
client message: "DYE_LASER >> close"  


### **************************  
### Wavemeter:
### **************************  
#### Message Examples:  
client message: "WAVEMETER >> read"    

