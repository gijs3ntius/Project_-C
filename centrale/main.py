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
        self.control_units = {}
        self.com_ports = []  # necessary to avoid adding existing com ports to the listener
        self.port_mapping = {}  # dictionary to keep track of the id's with the com ports
        self.supported_devices = ["Arduino Uno", "USB-SERIAL CH340"]

    def loop(self):
        # self.gui.register_ports(com_ports)  # register the comports to the gui
        while True:  # main loops that keeps running IN A LISTENER
            print(self.paused, self.control_units, self.com_ports, self.port_mapping)  # used for debugging purposes
            if  not self.paused:  # check if the program needs to be paused with listening to serial
                # --------------------------------------------------------------------------------------------------------------
                # main loop : part 1 : configuring the control_units
                # --------------------------------------------------------------------------------------------------------------
                # every iteration of the main loop all the ports are checked
                iteration_com_ports = []  # every iteration build an list with all the arduino's
                deletion_com_ports = []  # all the comports that are disconnected during the loop
                for port in list_ports.comports():  # port is here a comport connected to the central unit
                    # port[0] is the COMX
                    # port[1] is the name of the com port
                    iteration_com_ports.append(port[0])
                    if re.sub(r'\s+\(\w+\)', "", port[1]) in self.supported_devices:  # regular expression to check if the device is supported
                        if port[0] not in self.com_ports:  # TODO fix the problem with adding the arduino to another com port
                            self.control_units[port[0]] = SerialConnection(baudrate=19200, port=port[0])  # append an new SerialConnection
                            if self.control_units[port[0]] is None:  # if the connection failed remove the unit and the com port
                                del self.control_units[port[0]]
                                iteration_com_ports.remove(port[0])
                            # self.send_command(comport, Command.SET_ID, content)  # set ID to the control_unit
                self.com_ports = iteration_com_ports  # make sure the order and the value of the comports is updated
                # --------------------------------------------------------------------------------------------------------------
                # main loop : part 2 : reading the control_units
                # --------------------------------------------------------------------------------------------------------------
                # every iteration of the main loop all the control units are read
                for control_unit_port in self.control_units.keys():
                    try:  # try block used because there may occur read conflicts with the serial port
                        if control_unit_port not in self.com_ports: # if the comport is non existent add to remove list
                            deletion_com_ports.append(control_unit_port)
                            continue  # skip the rest of the code of this port
                        data = self.control_units[control_unit_port].receive()
                        if data == 0:  # if it is 0 something went wrong with receiving the data
                            continue  # continue to check the next control unit
                        # int.from_bytes(byte, byteorder='big' or byteorder='little') keep in mind little and big endian not important
                        header = int.from_bytes(data[0], byteorder='big')
                        content = int.from_bytes(data[1], byteorder='big')
                        control_unit_id = header >> 4  # SEE DATAPROTOCOL
                        sensor = header & 0x0F  # SEE DATAPROTOCOL
                        self.port_mapping[control_unit_id] = control_unit_port  # update port mapping
                        print(control_unit_id, self.port_mapping, sensor, content)  # for debugging purposes
                        # self.gui.update(control_unit_id, control_unit_port, sensor, value)  # gui needs to be updated
                    except Exception as e:
                        continue  # continues but does not use the data which could be false
                if len(deletion_com_ports) > 0:  # there are changes in the com_ports connected
                    # self.gui.notify_ports(self.com_ports)  # notify the gui of changes in the comports connected
                    for port in deletion_com_ports:  # delete all the items from the device dictionary that are not connected
                        try:
                            self.control_units[port].close()
                            del self.control_units[port]
                            self.com_ports.remove(port)
                        except Exception as e:
                            continue

    def loop_alternative(self):
        while True:
            if  not self.paused:
                com_ports = list(list_ports.comports())
                # mapping with comports is fixed when there is data received
                for com_port in com_ports:
                    if re.sub(r'\s+\(\w+\)', "", com_port[1]) in self.supported_devices:
                        connection = SerialConnection(baudrate=19200, port=com_port[0])
                        if connection is not None:
                            try:
                                data = connection.receive()
                            except Exception as e:
                                break  # TODO check if continue is better
                            if data == 0:  # if it is 0 something went wrong with receiving the data
                                continue  # continue to check the next control unit
                            # int.from_bytes(byte, byteorder='big' or byteorder='little') keep in mind little and big endian not important
                            header = int.from_bytes(data[0], byteorder='big')
                            content = int.from_bytes(data[1], byteorder='big')
                            control_unit_id = header >> 4  # SEE DATAPROTOCOL
                            sensor = header & 0x0F  # SEE DATAPROTOCOL
                            self.port_mapping[control_unit_id] = com_port[0]  # update port mapping
                            print(control_unit_id, self.port_mapping, sensor, content)  # for debugging purposes
                        connection.close()


    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def send_command(self, comport, command, content):
        self.pause()
        self.control_units[comport].send(command, content)
        self.unpause()


if __name__ == '__main__':
    test = 0  # this would be the GUI normally
    sl = SerialListener(test)
    sl.loop_alternative()
