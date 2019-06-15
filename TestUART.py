import serial
import struct
import time
#still in tests

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=2.0)

i = 0
while True:
    msg = struct.pack('>HBBB', 3000, 243, 234, 254)
    port.write(msg)
    time.sleep(0.3)

    bytesToRead = port.inWaiting()
    print("Found {} bytes in serial".format(bytesToRead))
    if bytesToRead == 5:
        rcv = port.read(5)
        # port.write('\r\nYou sent:' + repr(rcv))
        for i in range(5):
            print('\r {} - {}'.format(i, bytes(rcv[i])))

        idCode = struct.pack('BB', rcv[0], rcv[1])
        idCode = struct.unpack('>H', idCode)
        idCode = idCode[0]
        # value = struct.unpack_from('HBBB', decode)
    i += 1
    if i == 4:
        exit()
