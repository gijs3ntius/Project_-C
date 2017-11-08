from Serial import SerialConnection
from serial.tools import list_ports
from enum import Enum
import re

# A OBSERVER PATTERN NEEDS TO BE IMPLEMENTED TO GET THE GUI AND THE SERIAL LISTENER WORK TOGETHER
# THE LISTENER SHOULD PUSH DATA TO THE GUI EVERY TICK THERFOR THE GUI OBJECT SHOULD BE PASSED TO THE LISTENER
# THE LISTENER SHOULD CALL REGISTER ON THE GUI WHEN IT IS INITIALIZED
# I WILL START BUILDING THE LISTENER IN THE SAME FILE BUT IN A CLASS LISTENER OBVIOUSLY

class Command(Enum):
    SET_ID = 0
    ROL_OUT = 1
    ROL_IN = 2
    MAX_ROL_OUT = 3
    MIN_ROL_OUT = 4
    TEMP_ROL_IN = 5
    TEMP_ROL_OUT = 6
    LIGHT_ROL_IN = 7
    LIGHT_ROL_OUT = 8

class SensorType(Enum):
    LIGHT = 1
    TEMP = 2
    DIST = 3

class SerialListener:
    def __init__(self, GUI):
        # self.gui = GUI  # register the GUI to send data
        # GUI.register(self)  # register this object to the GUI, GUI will notify this object
        self.paused = False
        self.control_units = []
        self.supported_devices = ["Arduino Uno", "USB-SERIAL CH340"]

    def loop(self):
        com_ports = []  # necessary to avoid adding existing com ports to the listener
        while True:  # main loops that keeps running IN A LISTENER
            if  not self.paused:  # check if the program needs to be paused with listening to serial
                # --------------------------------------------------------------------------------------------------------------
                # main loop : part 1 : configuring the control_units
                # --------------------------------------------------------------------------------------------------------------
                # every iteration of the main loop all the ports are checked
                iteration_com_ports = []  # every iteration build an list with all the arduino's
                for port in list_ports.comports():  # port is here a comport connected to the central unit
                    # port[0] is the COMX
                    # port[1] is the name of the com port
                    iteration_com_ports.append(port[0])
                    if re.sub(r'\s+\(\w+\)', "", port[1]) in self.supported_devices:  # regular expression to check if the device is supported
                        if port[0] not in com_ports:
                            self.control_units.append([port[0], SerialConnection(baudrate=19200, port=port[0])])  # append an new SerialConnection
                com_ports = iteration_com_ports  # make sure the order and the value of the comports is updated
                # --------------------------------------------------------------------------------------------------------------
                # main loop : part 2 : reading the control_units
                # --------------------------------------------------------------------------------------------------------------
                # every iteration of the main loop all the control units are read
                for control_unit in self.control_units:
                    try:
                        data = control_unit.receive()
                        if data == 0:  # if it is 0 something went wrong with receiving the data
                            continue  # continue to check the next control unit
                        # int.from_bytes(byte, byteorder='big') keep in mind little and big endian not important
                        header = int.from_bytes(data[0], byteorder='big')
                        content = int.from_bytes(data[1], byteorder='big')
                        control_unit_id = header >> 4  # SEE DATAPROTOCOL
                        sensor = header & 0x0F  # SEE DATAPROTOCOL
                        print(control_unit_id, sensor, content)
                        # self.gui.notify(control_unit_id, sensor, value)  # gui needs to be updated
                    except Exception as e:
                        continue  # continues but does not use the data which could be false

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def send_command(self, comport, command, content):
        self.pause()
        self.connection
        self.unpause()

if __name__ == '__main__':
    test = 0  # this would be the GUI normally
    sl = SerialListener(test)
    sl.loop()
