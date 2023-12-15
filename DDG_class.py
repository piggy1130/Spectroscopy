import serial

class BaseDDGChannel:
    def __init__(self, channel_number):
        self.channel_number = channel_number
        self.state = None
        self.delay = None
        self.sync_channel = None
        self.width = None

    def set_state(self, state_status, connection, info_dict):
        self.state = state_status
        info_dict[f"DDG_channel_{self.channel_number}.state"] = state_status
        # msg = ":PULSE1:STAT ON\r\n"
        msg = f":PULSE{self.channel_number}:STAT {state_status}\r\n"
        connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        connection.readline()

    def set_delay(self, delay_value, connection, info_dict):
        self.delay = delay_value
        info_dict[f"DDG_channel_{self.channel_number}.delay"] = delay_value
        # msg = ":PULSE1:DEL -135e-6\r\n"
        msg = f":PULSE{self.channel_number}:DEL {delay_value}\r\n"
        connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        connection.readline()

    def set_sync_channel(self, channel, connection, info_dict):
        self.sync_channel = channel
        info_dict[f"DDG_channel_{self.channel_number}.sync_channel"] = channel
        msg = f":PULSE{self.channel_number}:SYNC {channel}\r\n"
        connection.write(str.encode(msg))
        connection.readline()

    def set_width(self, width_val, connection, info_dict):
        self.width = width_val
        info_dict[f"DDG_channel_{self.channel_number}.width"] = width_val
        # msg = ":PULSE1:WIDT 10e-6\r\n"
        msg = f":PULSE{self.channel_number}:WIDT {width_val}\r\n"
        connection.write(str.encode(msg))
        #after successfully setup, we could read msg b'ok\r\n'
        connection.readline()

# Specific channel classes inheriting from BaseDDGChannel
class DDG_channel_1(BaseDDGChannel):
    def __init__(self):
        super().__init__(1)

class DDG_channel_2(BaseDDGChannel):
    def __init__(self):
        super().__init__(2)

class DDG_channel_3(BaseDDGChannel):
    def __init__(self):
        super().__init__(3)

class DDG_channel_4(BaseDDGChannel):
    def __init__(self):
        super().__init__(4)

class DDG_channel_5(BaseDDGChannel):
    def __init__(self):
        super().__init__(5)

class DDG_channel_6(BaseDDGChannel):
    def __init__(self):
        super().__init__(6)

class DDG_channel_7(BaseDDGChannel):
    def __init__(self):
        super().__init__(7)

class DDG_channel_8(BaseDDGChannel):
    def __init__(self):
        super().__init__(8)


class DDG:
    connection = serial.Serial('/dev/ttyUSB0', 115200)

    def __init__(self):
        self.channels = {
            1: DDG_channel_1(),
            2: DDG_channel_2(),
            3: DDG_channel_3(),
            4: DDG_channel_4(),
            5: DDG_channel_5(),
            6: DDG_channel_6(),
            7: DDG_channel_7(),
            8: DDG_channel_8(),                               
        }
        self.DDG_Initialization()

    def DDG_Initialization(self, info_dict):

        self.channels[1].set_state("ON", self.connection, info_dict)
        # ... Rest of the initialization ...

