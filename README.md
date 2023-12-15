# Spectroscopy
Got the spectroscopy data from scanning 

### Client Desktop use GUI
## Table 1 (Linux) - DDG, SCOPE, DYE-LASER, SHUTTER & DATABASE
## Table 2 (Windows) - WAVEMETER

# The Overall Structure
1. We use GUI to talk to "Table 1" only.
2. "Table 1" talks to "Table 2" for any work that needs to be done related to "Table 2"

# Running Process
1. Start the "Table 2" python file first since it also works as the server for "Table 1"
2. Start the "Table 1" python file
   
1. Start the “Server Program” in Table2_windows
    “server_table2(Windows)_WAVEMETER_1030”
    Note: we use table_1 to communicate with table_2. In this communication, table_1 works as the client and table_2 works as the server. We need to start the server before the client.
With this communication, the master client only needs to talk to table_1.
“server_table2(Windows)_WAVEMETER_1030”
(needs the head file “wlm.py”)

2. Start the “Server Program” in Table1_linux
“server_table1(linux)_DDG_SCOPE_LASER_SHUTTER_1030”

3. Start to send requests from Client Windows Desktop
“Client_Wavelength_Scan_ReadToUse_1030”



