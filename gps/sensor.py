from arduino_communicable import ArduinoCommunicable

class Sensor(ArduinoCommunicable):
    def parseValue(self, string):
        return super().parseValue(string)

    def update(jsonFromArduino):
        """ Here we must update the sensor to reflect what the arduino gives us 
        """
        pass
