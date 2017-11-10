from connections import SerialConnection
from serial.tools import list_ports
from enums import Command
import time
import re

class SerialControler:
    def __init__(self, GUI):
        self.__paused__ = False
        self.control_units = {}
        self.supported_devices = ["Arduino Uno", "USB-SERIAL CH340"]

    def connect_ports(self):
        for port in list(list_ports.comports()):
            if re.sub(r'\s+\(\w+\)', "", port[1]) in self.supported_devices:
                if port[0] not in self.control_units.keys():
                    self.control_units[port[0]] = SerialConnection(baudrate=19200, port=port[0])
        return self.control_units.keys()  # returns the com ports

    def read_ports(self):
        if not self.__paused__:
            data_list = []
            print(self.control_units.keys())
            for port in self.control_units.keys():
                try:
                    data = self.control_units[port].receive()
                except Exception as e:
                    del self.control_units[port]  # remove this device
                    break;  # break out of the for to update the com_ports
                if data == 0:  # if it is 0 something went wrong with receiving the data
                    continue  # continue to check the next control unit
                header = int.from_bytes(data[0], byteorder='big')
                content = int.from_bytes(data[1], byteorder='big')
                control_unit_id = header >> 4  # SEE DATAPROTOCOL
                sensor = header & 0x0F  # SEE DATAPROTOCOL
                data_list.append([port, sensor, content])
                # print(control_unit_id, "type:", sensor, "value:", content)  # for debugging purposes
            return data_list

    def __debug_read_data__(self):
        for device in self.control_units.values():
            try:
                data = device.receive()
            except Exception as e:
                continue  # break out of the for to update the com_ports
            if data == 0:  # if it is 0 something went wrong with receiving the data
                continue  # continue to check the next control unit
            print("{0:b}".format(int.from_bytes(data[0], byteorder='big')), ":", "{0:b}".format(int.from_bytes(data[1], byteorder='big')), "\n")

    def __pause__(self):
        self.__paused__ = True

    def __unpause__(self):
        self.__paused__ = False

    def send_command(self, com_port, command, content):
        self.__pause__()
        if command is Command.MAX_ROL_OUT or command is Command.MAX_ROL_OUT:
            self.control_units[com_port].send(command, content >> 2)  # shift the value becaue content can vary 2 -> 400
        else:
            self.control_units[com_port].send(command, content)
        self.__unpause__()

    def getConnectedDevices(self):
        return self.control_units


# only here for debugging purposes
if __name__ == '__main__':
    test = 0  # this would be the GUI normally
    sl = SerialControler(test)
    sl.connect_ports()
    print(sl.getConnectedDevices())
    sl.__debug_read_data__()
    number = 0
    while True:
        number += 1
        print(number)
        if number % 7 == 0:
            sl.connect_ports()
            print(sl.getConnectedDevices())
            time.sleep(0.1)
        # sl.debug_read_data()
        sl.read_ports()
        time.sleep(0.1)
