from Serial import SerialConnection
from serial.tools import list_ports
from enum import Enum
import time
import re

# A OBSERVER PATTERN NEEDS TO BE IMPLEMENTED TO GET THE GUI AND THE SERIAL LISTENER WORK TOGETHER
# THE LISTENER SHOULD PUSH DATA TO THE GUI EVERY TICK THERFOR THE GUI OBJECT SHOULD BE PASSED TO THE LISTENER
# THE LISTENER SHOULD CALL REGISTER ON THE GUI WHEN IT IS INITIALIZED
# I WILL START BUILDING THE LISTENER IN THE SAME FILE BUT IN A CLASS LISTENER OBVIOUSLY

class SerialListener:
    def __init__(self, GUI):
        # self.gui = GUI  # register the GUI to send data
        # GUI.register(self)  # register this object to the GUI, GUI will notify this object
        self.paused = False
        self.control_units = {}
        # self.com_ports = []  # necessary to avoid adding existing com ports to the listener
        # self.port_mapping = {}  # dictionary to keep track of the id's with the com ports
        self.supported_devices = ["Arduino Uno", "USB-SERIAL CH340"]

    def connect_ports(self):
        for port in list(list_ports.comports()):
            if re.sub(r'\s+\(\w+\)', "", port[1]) in self.supported_devices:
                if port[0] not in self.control_units.keys():
                    self.control_units[port[0]] = SerialConnection(baudrate=19200, port=port[0])

    def read_ports(self):
        data = []
        for device in self.control_units.values():
            try:
                data = device.receive()
            except Exception as e:
                continue  # break out of the for to update the com_ports
            if data == 0:  # if it is 0 something went wrong with receiving the data
                continue  # continue to check the next control unit
            header = int.from_bytes(data[0], byteorder='big')
            content = int.from_bytes(data[1], byteorder='big')
            control_unit_id = header >> 4  # SEE DATAPROTOCOL
            sensor = header & 0x0F  # SEE DATAPROTOCOL
            data.append([control_unit_id, sensor, content])
            print(control_unit_id, "type:", sensor, "value:", content)  # for debugging purposes
        return data

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def send_command(self, comport, command, content):
        self.pause()
        self.control_units[comport].send(command, content)
        self.unpause()

    def getConnectedDevices(self):
        return self.control_units


# only here for debugging purposes
if __name__ == '__main__':
    test = 0  # this would be the GUI normally
    sl = SerialListener(test)
    sl.connect_ports()
    print(sl.getConnectedDevices())
    while True:
        sl.read_ports()
        time.sleep(0.1)
