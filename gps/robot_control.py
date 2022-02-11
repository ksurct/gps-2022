
class RobotControl():
    def __init__(self, name):
        self.name = name
        pass

    #From arduino
    def getSensorData(self):
        pass

    def updateFromArduino(self):
        pass

    def rotate(degrees, speed):
        # set motors LF and LB -100
        # set motors RF and RB 100
        pass

    def move(meters, speed):
        pass

    def getCameraData(self):
        pass

    def getAngle(self):
        pass

    def getSpeed(self):
        pass

    def getLocation(self):
        pass

    def setSpeed(self, speed):
        pass


robot1 = RobotControl("Name1")
robot2 = RobotControl("Name2")

