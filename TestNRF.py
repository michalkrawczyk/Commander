from NRF24L01.nrf24 import NRF24
import time
import struct

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0x0a, 0x0a, 0x0a, 0x0a, 0x0a]]

radio = NRF24()
radio.begin(0, 0, 17, 27)  # Set CE and IRQ pins
radio.setRetries(15, 15)
radio.setPayloadSize(5)
# radio.setChannel(0x02)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)


def writeMode():
    radio.stopListening()
    radio.openWritingPipe(pipes[1])
    #radio.openReadingPipe(1, pipes[0])

   # radio.startListening()
   # radio.stopListening()


def listenMode():
    radio.openWritingPipe(pipes[0])
    #radio.openReadingPipe(1, pipes[1])

    radio.startListening()
   # radio.stopListening()
    #radio.startListening()

i = 0
while True:
    print(i)
    #listenMode()
    #print("Listen Mode")
    #recv_buffer = []
    #pipe = [0]
    #time.sleep(0.2)
    #if radio.available(pipe, True):
    #    print("Radio Available")
    #    radio.read(recv_buffer)
    #   # values = struct.unpack_from('HBBB',"".join(recv_buffer))
    #    print(*recv_buffer)
       # print(values)
    #else:
    writeMode()
    print("Write Mode")
    msg = struct.pack('HBBB', 3000, 243, 234, 254)
    msg=0x09
    input()
    a=radio.write(msg)
    print(a)
    time.sleep(0.2)
    i += 1
    if i == 4:
        exit()
