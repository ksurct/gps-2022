from motor import Motor
import time

class Robot():
    def __init__(self):
        self.right = Motor(13,24)
        self.left = Motor(12,23)
        self.timeCalled = time.time()
        self.timeToKill = 0

    # Compass
    def getAngle(self):
        pass

    # GPS Data
    def getPosition(self):
        pass

    # Sensor data
    # Return Dictionary
    def getSensorData(self):
        pass

    # Camera data, return camera -> splits -> objects
    def getCameraData(self):
        pass

    def mpsToPercent(self, speedMps):
        return 4 / 0.78 * speedMps

    def angleToPercent(self):
        pass

    # Tells wether the robot is executing a move
    def isNotMoving(self):
        return self.stopped
    
    # Set constant speed
    def constantMove(self, speed):
        pass

    # Set constant rotation
    def constantRotate(self, speed):
        pass

    # Move a certain distance at a speed
    def move(self, speedMps, distanceMeters):
        speedPercent = self.mpsToPercent(speedMps)
        seconds = distanceMeters / speedMps
        self.right.setSpeed(speedPercent)
        self.left.setSpeed(speedPercent)
        self.timeCalled = time.time()
        self.timeToKill = seconds
        print("Kill after", self.timeToKill)



    # Rotate a certain amount at a certain speed
    def rotate(self, speed, degrees):
        pass

    # Stop the robot
    def stop(self):
        self.left.setSpeed(0)
        self.right.setSpeed(0)

    def tick(self):
        print("Time: ", time.time())
        print("Called time: ", self.timeCalled)
        if (time.time() - self.timeCalled > self.timeToKill):
            self.stop()
            return 0
        return 1

class Camera():
    def __init__(self):
        pass

    # Get data from camera
    def getData(self):
        pass

if __name__ == '__main__':
    from RPi import GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    robot = Robot()
    robot.move(0.78/4, 2)
    while(robot.tick()):
        time.sleep(0.1)
