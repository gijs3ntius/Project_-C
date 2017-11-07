from Serial import SerialConnection
from serial.tools import list_ports

# A OBSERVER PATTERN NEEDS TO BE IMPLEMENTED TO GET THE GUI AND THE SERIAL LISTENER WORK TOGETHER
# THE LISTENER SHOULD PUSH DATA TO THE GUI EVERY TICK THERFOR THE GUI OBJECT SHOULD BE PASSED TO THE LISTENER
# THE LISTENER SHOULD CALL REGISTER ON THE GUI WHEN IT IS INITIALIZED
# I WILL START BUILDING THE LISTENER IN THE SAME FILE BUT IN A CLASS LISTENER OBVIOUSLY

class SerialListener:
    def __init__(self, GUI):
        # self.gui = GUI  # register the GUI to send data
        # GUI.register(self)  # register this object to the GUI, GUI will notify this object
        self.paused = False
        self.control_units = []
        pass

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
                    iteration_com_ports.append(port[0])
                    # port[0] is the COMX
                    # port[1] is the name of the com port
                    if "Arduino" in port[1] or "arduino" in port[1] or "USB-SERIAL CH340" in port[1]:  # if the com port is communicating with an arduino
                        if port[0] not in com_ports:
                            self.control_units.append(SerialConnection(baudrate=19200, port=port[0]))  # append an new SerialConnection
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
                        # int.from_bytes(byte, byteorder='big') keep in mind little and big endian
                        print(data)
                        # control_unit_id = data[0] >> 4
                        # sensor = data[0] & 0x0F
                        # value = data[1]  # SEE DATAPROTOCOL
                        # self.gui.notify(control_unit_id, sensor, value)  # gui needs to be updated
                    except Exception as e:
                        continue

    def pause():
        self.paused = True

    def unpause():
        self.paused = False

if __name__ == '__main__':
    test = 0  # this would be the GUI normally
    sl = SerialListener(test)
    sl.loop()
