from Project.Serial import SerialConnection

if __name__ == '__main__':
    serial = SerialConnection(19200, 'COM5')
    print(serial.send(5, 6))