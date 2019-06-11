import serial
from DatabaseConnection.dbConn import *
from NRF24L01.commandGenerator import *
import time
import struct

# TODO: change database address
database = 'H:\\PycharmProjects\\Projekt_Zespolowy\\db.sqlite3'

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

devicesOut = [
    newRGBLamp(2),
    newBlinds(3)
]
devicesIn = [
    newTempSensor(4)
]

conn = create_connection(database)
with conn:
    while True:
            data = getLastCurrentData(conn)

            if data.manualControl:
                print("Data taken from Database")
                for dev in devicesOut:
                    if dev.group == Group.RGB_LAMPS:
                        msg = pack('>HBBB', dev.numericView(), data.red, data.blue, data.green)
                        port.write(msg)
                    elif dev.group == Group.BLINDS:
                        msg = pack('>HBBB', dev.numericView(), 0, data.shutterPosition, 0)  # Todo:Check
                        port.write(msg)
                    time.sleep(0.1)
            else:
                print("Data taken from Sensors")
                recv_buffer = []
                with port:
                    recv_buffer = port.read(7)  # TODO : Zabezpieczenie? Sprawdzic ile bajtow przyjdzie
                    if recv_buffer:
                        msg = struct.unpack_from('HfB', recv_buffer)

                        if msg[0] == devicesIn[0]:  # Change in future
                            temperature = msg[1]
                        else:  # ciii
                            temperature = 20  # Default

                        for dev in devicesOut:
                            if dev.group == Group.RGB_LAMPS or dev.group == Group.BLINDS:
                                msg = commandBytes(dev.deviceID, dev.group, temperature)
                                port.write(msg)
                            time.sleep(0.1)
                    # port.read()  # clear data TODO: sprawdzic czy potrzebne



