
class ArduinoCommunicable():
    def __init__(self, name):
        self.name = name
        self.value = None
        self.valid = False

    def parseValue(self, string):
        pass

    def update(self, jsonFromArduino):
        self.value
        self.valid = self.parseValue(jsonFromArduino[self.name]['valid'])
        self.value = jsonFromArduino[self.name]['value']

    def isValid(self):
        return self.valid
