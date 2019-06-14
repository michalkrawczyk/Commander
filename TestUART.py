import serial
import struct
import sys

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

i = 0
while True:
    msg = struct.pack('>HBBB', 3000, 243, 234, 254)
    #print(port.getsettings())
    print(port.readable())
    print(port.writeable())
    print(port.isopen)
    #b=(3).to_bytes(1,byteorder='big')
    #port.write(b)
    #rcv = port.read(5)
    #print(rcv)
   # rcv = int.from_bytes(rcv, byteorder='big')
    #port.write('\r\nYou sent msg' + str(rcv) +'\n' )
    #value = struct.unpack('>HBBB',rcv)
   # print("Lenght:")
   # print(len(rcv))
    #print("rcv")
    #print("\n"+str(rcv))
    #print("Raspberry got:")
    i += 1
    if i == 4:
        print('\r\n')
        exit()
