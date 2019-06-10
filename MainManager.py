from NRF24L01.nrf24 import NRF24
from DatabaseConnection.dbConn import *
from NRF24L01.commandGenerator import *
import time

#TODO: co z roleta?
database = 'H:\\PycharmProjects\\Projekt_Zespolowy\\db.sqlite3'

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24()
radio.begin(1, 0, "P8_23", "P8_24") #Set CE and IRQ pins
radio.setRetries(15, 15)
radio.setPayloadSize(5)
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


conn = create_connection(database)
with conn:
    while True:
        data = getLastCurrentData(conn)

        if data.manualControl:
            for dev in devicesOut:
                if dev.group == Group.RGB_LAMPS:
                    msg = pack('>HBBB', dev.numericView(), data.red, data.blue, data.green)
                    radio.write(msg)
                    time.sleep(0.1)
                # TODO:if Roleta
        else:
           listenMode()
           #TODO : on Listen ModE




