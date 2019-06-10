from NRF24L01.nrf24 import NRF24
import time

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24()
radio.begin(1, 0, "P8_23", "P8_24")  # Set CE and IRQ pins
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

    while True:
        listenMode()
        recv_buffer = []
        pipe = [0]
        if radio.available(pipe, True):
            radio.read(recv_buffer)
        else:
            writeMode()
            radio.write('\x02\x84\xff\xff\xfb')
            time.sleep(0.2)
