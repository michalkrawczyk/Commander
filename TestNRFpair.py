
from NRF24L01.nrf24 import NRF24
from DatabaseConnection.dbConn import *
from NRF24L01.commandGenerator import *
import time


# Initialize Database Connection
database = 'H:\\PycharmProjects\\Projekt_Zespolowy\\db.sqlite3'
conn = create_connection(database)

# Initialize NRF

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2], [0xc2, 0xc2, 0xc2, 0xc2, 0xc3]]

    #Radio-Sender
radioSender= NRF24()
radioSender.begin(1, 0, "P8_23", "P8_24")

radioSender.setRetries(15, 15)
radioSender.setPayloadSize(NRF24.MAX_PAYLOAD_SIZE)
radioSender.setChannel(0x60)
radioSender.setDataRate(NRF24.BR_250KBPS)

radioSender.setAutoAck(1)
radioSender.enableDynamicPayloads()
radioSender.enableAckPayload()

radioSender.openWritingPipe(pipes[2])
radioSender.openReadingPipe(1,pipes[0])


def sendToBlinds(deviceID,group,temperature):
    buf = commandBytes(deviceID,group,temperature)
    #albo commandNumeric
    radioSender.write(buf)
    print("Sending message to blinds")
    if radioSender.isAckPayloadAvailable():
        pl_buffer = []
        radioSender.read(pl_buffer, radioSender.getDynamicPayloadSize())
        print("\033[31;1mPTX Received back:\033[0m"),
        print(pl_buffer)
    else:
        print("PTX Received: Ack only, no payload")

def sendToRGBLamp(deviceID,group,temperature):
    buf = commandBytes(deviceID,group,temperature)
    # albo commandNumeric
    radioSender.write(buf)
    print("Sending message to lamp")
    if radioSender.isAckPayloadAvailable():
        pl_buffer = []
        radioSender.read(pl_buffer, radioSender.getDynamicPayloadSize())
        print("\033[31;1mPTX Received back:\033[0m"),
        print(pl_buffer)
    else:
        print("PTX Received: Ack only, no payload")



    #Radio-Receiver
radioReceiver = NRF24()
radioReceiver.begin(1, 0, "P8_23", "P8_24")

radioReceiver.setRetries(15, 15)
radioReceiver.setPayloadSize(NRF24.MAX_PAYLOAD_SIZE)
radioReceiver.setChannel(0x60)
radioReceiver.setDataRate(NRF24.BR_250KBPS)

radioReceiver.setAutoAck(1)
radioReceiver.enableDynamicPayloads()
radioReceiver.enableAckPayload()

radioReceiver.openWritingPipe(pipes[0])
radioReceiver.openReadingPipe(1, pipes[1])


radioReceiver.startListening()

radioReceiver.printDetails()

def receive():
    pipe = [0]
    if not radioReceiver.available(pipe):
        return

    recv_buffer = []
    radioReceiver.read(recv_buffer, radioReceiver.getDynamicPayloadSize())
    print("\033[32;1mPRX Received:\033[0m"),
    print(recv_buffer)


test = 0
while True:
    test += 1
    print("Loop:" + str(test))
    # Todo: pozyskaj dane z bazy , wprowadz temperature i wypadek kiedy nie nastawia pomiarow
    sendToBlinds(3, Group.BLINDS, 20)
    time.sleep(0.05)
    sendToRGBLamp(4,Group.RGB_LAMPS, 20)
    time.sleep(0.05)
    receive()
    time.sleep(0.05)
