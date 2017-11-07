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

    def open(self):
        self.connection.open()

    def close(self):
        self.connection.close()

    def send(self):
        pass

    def receive(self):
        pass
