from datetime import datetime
from NRF24L01.IdentifierFrame import *
from struct import *


def calculateRGB(temperature, illuminance):
    now = datetime.now()
    am11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
    am9 = now.replace(hour=9, minute=0, second=0, microsecond=0)
    pm7 = now.replace(hour=19, minute=0, second=0, microsecond=0)
    pm4 = now.replace(hour=16, minute=0, second=0, microsecond=0)
    pm10 = now.replace(hour=22, minute=0, second=0, microsecond=0)

    # Lights
    directSunlight = [255, 255, 255]
    highNoonSun = [255, 255, 251]
    halogen = [255, 241, 224]
    warmWhite = [255, 172, 58]
    candle = [255, 147, 41]
    noLight = [0, 0, 0]

    color = noLight

    if temperature > 14:
        if am9 <= now < am11:
            color = warmWhite
        elif pm7 <= now < pm10:
            color = candle
    else:
        if am9 <= now < am11:
            color = halogen
        elif am11 <= now < pm4:
            color = highNoonSun
        elif pm4 <= now < pm7:
            color = warmWhite
        elif pm7 <= now < pm10:
            color = candle

    if illuminance >= 2000:
        color = noLight
    elif illuminance < 1000 and (am11 <= now < pm4):
        color = directSunlight

    return color


def calculateBlindsPosition(temperature, cloudness , illuminance):
    manual = False

    now = datetime.now()
    am11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
    am9 = now.replace(hour=9, minute=0, second=0, microsecond=0)
    pm7 = now.replace(hour=19, minute=0, second=0, microsecond=0)
    pm4 = now.replace(hour=16, minute=0, second=0, microsecond=0)
    pm10 = now.replace(hour=22, minute=0, second=0, microsecond=0)

    position = 100
    # 100 to w pelni zasloniete

    if temperature > 14:
        if am9 <= now < am11:
            position = 0
        elif am11 <= now < pm4:
            position = 25 - int(cloudness/4)
        elif pm4 <= now < pm7:
            position = 0
        elif pm7 <= now < pm10:
            position = 50
    else:
        if am9 <= now < am11:
            position = 25 - int((100-cloudness)/4)
        elif am11 <= now < pm4:
            position = 0
        elif pm4 <= now < pm7:
            position = 75

    if position < 50 and cloudness > 70:
        position = 50

    if illuminance > 2000:
        position = (position + 20) % 100

    result = [int(manual), position, 0]
    return result


def commandNumeric(deviceID, group, temperature, cloudness=0, illuminance=1500):
    identifier = Identifier(True, group, deviceID)
    result = [identifier.numericView()]
    if group == Group.BLINDS:
        result.extend(calculateBlindsPosition(temperature, cloudness, illuminance))
    if group == Group.RGB_LAMPS:
        result.extend(calculateRGB(temperature, illuminance))
    return result


def commandBytes(deviceID, group, temperature, cloudness=0, illuminance=1500):
    identifier = Identifier(True, group, deviceID)
    result = 0
    if group == Group.BLINDS:
        result = pack('>HBBB', identifier.numericView(), *calculateBlindsPosition(temperature, cloudness, illuminance))
    if group == Group.RGB_LAMPS:
        result = pack('>HBBB', identifier.numericView(), *calculateRGB(temperature, illuminance))
    return result

