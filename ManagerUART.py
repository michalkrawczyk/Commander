import serial
from DatabaseConnection.dbConn import *
from NRF24L01.commandGenerator import *
import time
import struct

# TODO: change database address
database = 'H:\\PycharmProjects\\Projekt\\db.sqlite3'

port = serial.Serial("COM3", baudrate=115200, timeout=1.0)

# devicesOut = [
#     newRGBLamp(2),
#     newBlinds(3)
# ]
# devicesIn = [
#     newTempSensor(4)
# ]

# lampAddr = [0x0A, 0x0A, 0x0A, 0x0A, 0x0A]
# blindAddr = [0x0A, 0x0A, 0x06, 0x06, 0x06]

conn = create_connection(database)
with conn:
    while True:
            data = getLastCurrentData(conn)
            print(data.manualControl)
            if data.manualControl:
                print("Data taken from Database")
                # for dev in devicesOut:
                    # if dev.group == Group.RGB_LAMPS:
                    #     msg = pack('>HBBB', *lampAddr, dev.numericView(), data.red, data.blue, data.green)
                    #     port.write(msg)
                    # elif dev.group == Group.BLINDS:
                    #     #msg = pack('>HBBB', *blindAddr, dev.numericView(), 0, data.shutterPosition, 0)  # Todo:Check
                    #     msg = pack('>BBBH', *blindAddr, 0, data.shutterPosition, 0, 0, 0)
                    #     port.write(msg)
                    # time.sleep(0.1)
                msg = struct.pack('BBBBB', 1, data.shutterPosition, data.red, data.green, data.blue)
                port.write(msg)
                time.sleep(6)
            else:
                print("Data taken from Sensors")
                #recv_buffer = []
                with port:
                    # recv_buffer = port.read(10)  # TODO : Zabezpieczenie? Sprawdzic ile bajtow przyjdzie
                    # if recv_buffer:
                    #    msg = struct.unpack_from('HfB', recv_buffer)
                    #
                    #     if msg[0] == devicesIn[0]:  # Change in future
                    #         temperature = msg[1]
                    #     else:  # ciii
                    #         temperature = 20  # Default
                    #
                    #     for dev in devicesOut:
                    #         if dev.group == Group.RGB_LAMPS or dev.group == Group.BLINDS:
                    #             msg = commandBytes(dev.deviceID, dev.group, temperature)
                    #             port.write(msg)
                    #         time.sleep(0.1)
                    # port.read()  # clear data TODO: sprawdzic czy potrzebne
                    msg = withoutID(data.temperature, 25)
                    print(msg)
                    port.write(msg)
                    time.sleep(6)


