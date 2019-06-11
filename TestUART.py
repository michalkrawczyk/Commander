import serial
import struct

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

i = 0
while True:
    msg = struct.pack('HBBB', 3000, 243, 234, 254)
    port.write(msg)
    rcv = port.read(7)
    port.write('\r\nYou sent:' + repr(rcv))
    value = struct.unpack_from('HBBB', rcv)
    print("Raspberry got:")
    print(value)
    i = +1
    if i == 4:
        exit()
