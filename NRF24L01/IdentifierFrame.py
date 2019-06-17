from enum import IntEnum
import struct

def getBit(value: int, index: int):
    digit = (value & (1 << index)) >> index
    return digit


class Group(IntEnum):
    NONE = 0
    LAMPS = 1
    RGB_LAMPS = 2
    BLINDS = 3
    TEMPERATURE_SENSORS = 4
    ILLUMINANCE_SENSORS = 5


class Identifier:
    def __init__(self, master: bool, group: Group, deviceID):
        if deviceID > 511 or deviceID < 0:
            raise ValueError("Class:Identifier - Wrong argument of ID")
        if group > 64 or group < 0:
            raise ValueError("Class:Identifier - Wrong argument of group")
        if master != 0 and master != 1:
            raise ValueError("Class:Identifier - Wrong argument of master")

        self.master = master
        self.group = group
        self.deviceID = deviceID

    @classmethod
    def fromIdentifierFrame(cls, identifier):
        # Todo Zabezpieczenia
        master = getBit(identifier, 15)
        group = 0
        deviceID = 0

        for i in range(6):
            group = group | (getBit(identifier, 9 + i) << i)
        for i in range(9):
            deviceID = deviceID | (getBit(identifier, i) << i)

        return cls(bool(master), group, deviceID)

    def __str__(self):
        return "ID:"+str(self.deviceID) + " Group:" + str(self.group) + " Master:" + str(self.master)

    def numericView(self):
        bitMaster = self.master << 15
        bitGroup = self.group << 9
        bitID = self.deviceID

        result = bitMaster | bitGroup | bitID
        return result


def newRGBLamp(deviceID):
    return Identifier(True,Group.RGB_LAMPS, deviceID)


def newBlinds(deviceID):
    return Identifier(True, Group.BLINDS, deviceID)


def newTempSensor(deviceID):
    return Identifier(False, Group.TEMPERATURE_SENSORS, deviceID)
