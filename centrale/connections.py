import serial, time

'''
Version: 1.0.0
Author: Stephan Hilberts & Gijs Entius
Date: 07 Nov 2017
'''


class SerialConnection:
    """
    Init constructor of the SerialConnection class.
    @param: baudrate, port (we are using 19200 as baudrate
    Saves the baudrate and port in their variables when an object is created for later use.
    Sets up a connection using the baudrate and port of the object.
    """

    def __init__(self, baudrate, port):
        self.baudrate = baudrate  # we are using 19200 as baudrate
        self.port = port
        try:
            self.connection = serial.Serial(baudrate=baudrate, port=port)  # setting up connection with port and baudrate.
        except Exception as e:
            return None  # return 0 to indicate the connection failed
        # self.connection.open() apparently it is already opened
        self.serialBusy = False

    """
    Function to check the connected port
    """

    def port_connected(self):
        print(self.connection.port)  # prints to what port you are connected

    """
    Function to open the serial connection
    """

    def open(self):
        self.connection.open()  # opens the connection

    """
    Function to close the serial connection
    """

    def close(self):
        self.connection.close()  # closes the connection

    """
    Function to send command data to the Arduino
    @param: command(commands are listed using ENUM and will use the index of the command)
            value(the data type integer is used for value)
    This function will convert the [command, value] list to bytes in order to send them to the Arduino.
    serialBusy is set and used to check if the program is busy.
    This function has been tested and is able to send both the hexvalues of the command and value over serial
    """

    def send(self, command, value):
        command_value = bytes([command, value])  # build command and value to bytes to make it transferable
        if not self.serialBusy:
            self.serialBusy = True  # makes sure nothing is done on serial on this moment
            self.connection.write(command_value)  # writes the command and the value in bytes to the serial output
            # time.sleep(1)  # wait 1 sec for the Arduino to get the command
            # self.connection.write(bytes([value]))
            self.serialBusy = False  # makes serial available again
            return 1  # serial finished successfully
        else:
            return 0  # serial is already doing something

    """
    Function to receive data from the Arduino.
    This function will receive 2 datablocks of 1 byte/ 8 bits each time and add these to the data list.
    First datablock: first 4 bits = ID of Arduino, last 4 bits = data format
    Last datablock: all 8 bits contain the data
    """

    def receive(self):
        if not self.serialBusy:
            self.serialBusy = True  # makes sure nothing is done on serial on this moment
            data = []  # init the list where the received data will be saved
            block_part = self.connection.read(size=1)  # reading the data in parts of 8 bits / 1 byte
            data.append(block_part)  # adding received data to the list
            block_part = self.connection.read(size=1)  # reading the data in parts of 8 bits / 1 byte
            data.append(block_part)  # adding received data to the list
            self.serialBusy = False  # makes serial available again
            return data
        else:
            return 0  # serial is already doing something
