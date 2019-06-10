class CurrentData:
    def __init__(self, red, green, blue, temperature, shutterState, manualControl):
        self.manualControl = manualControl
        self.shutterState = shutterState
        self.temperature = temperature
        self.blue = blue
        self.green = green
        self.red = red

    def __str__(self):
        return "RGB:("+str(self.red)+","+str(self.blue)+","+str(self.green)+")"

# Todo: Sensor , ErrorData, ?DEVICE?
