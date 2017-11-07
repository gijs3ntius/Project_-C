import serial

'''
Version: 1.0.0
Author: Stephan Hilberts & Gijs Entius
Date: 07 Nov 2017
'''


class SerialConnection:
    """
    Init constructor of the SerialConnection class.
    @param: baudrate, port
    Saves the baudrate and port in their variables when an object is created for later use.
    Sets up a connection using the baudrate and port of the object.
    """
    def __init__(self, baudrate, port):
        self.baudrate = baudrate
        self.port = port
        self.connection = serial.Serial(baudrate=baudrate, port=port)  # setting up connection with port and baudrate.
        self.connection.open()

    def portcheck(self):
        print("Connected to: " + self.connection.port)  # prints to what port you are connected

    def open(self):
        self.connection.open()  # opens the connection

    def close(self):
        self.connection.close()  # closes the connection

    def send(self, command, value):
        pass  # sending 8 bits at a time, waiting for another function to use here

    def receive(self):
        data = []  # init the list where the received data will be saved
        block_part = self.connection.read(size=1)  # reading the data in parts of 8 bits / 1 byte
        data.append(block_part)  # adding received data to the list
        block_part = self.connection.read(size=1)  # reading the data in parts of 8 bits / 1 byte
        data.append(block_part)  # adding received data to the list
        return data





