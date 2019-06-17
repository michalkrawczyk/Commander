from NRF24L01.nrf24 import NRF24
from DatabaseConnection.dbConn import *
from NRF24L01.commandGenerator import *
import time
import struct

# TODO: change database address
database = 'H:\\PycharmProjects\\Projekt\\db.sqlite3'

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0x0A, 0x0A, 0x0A, 0x0A, 0x0A], [0x0A, 0x0A, 0x06, 0x06, 0x06]]


radio = NRF24()
radio.begin(1, 0, 17, 27)  # Set CE and IRQ pins
radio.setRetries(15, 15)
# radio.setPayloadSize(7)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)


def writeMode():
    radio.stopListening()
    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[0])

    # radio.startListening()
    # radio.stopListening()


def listenMode():
    radio.openWritingPipe(pipes[0])
    radio.openReadingPipe(1, pipes[1])

    # radio.startListening()
    # radio.stopListening()

    radio.startListening()


# while True:
#     listenMode()
#     pipe = [0]
#     if radio.available(pipe,True):
#         recv_buffer = []
#         radio.read(recv_buffer)
#
#     else:
#         writeMode()
#         radio.write(b'\x02\x84\xff\xff\xfb')
#         time.sleep(0.5)

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
                    radio.write(msg)
                elif dev.group == Group.BLINDS:
                    msg = pack('>HBBB', dev.numericView(), data.red, data.blue, data.green)
                    radio.write(msg)
                time.sleep(0.1)
        else:
            print("Data taken from Sensors")
            listenMode()
            pipe = [0]
            if radio.available(pipe, True):
                recv_buffer = []
                radio.read(recv_buffer, 7)  # TODO : Zabezpieczenie? Sprawdzic ile bajtow przyjdzie

                if recv_buffer:
                    msg = struct.unpack_from('HfB', recv_buffer) # Insert into sensors

                    if msg[0] == devicesIn[0]: # Change in future
                        temperature = msg[1]
                    else:  # ciii
                        temperature = 20  # Default

                    writeMode()

                    for dev in devicesOut:
                        if dev.group == Group.RGB_LAMPS or dev.group == Group.BLINDS:
                            msg = commandBytes(dev.deviceID, dev.group, temperature)
                            radio.write(msg)
                        time.sleep(0.1)
