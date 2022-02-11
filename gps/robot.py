#from motor import Motor

class Robot():
    def __init__(self):
        self.stopped = True

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
        ret = {}
        for camera in self.cameras.keys():
            self.cameras[camera].update(self, -self.robotBody.angle+pi/2, self.course)
            ret[camera] = self.cameras[camera].getData()
        return ret

    # Tells wether the robot is executing a move
    def isNotMoving(self):
        return self.stopped
    
    # Set constant speed
    def constantMove(self, speed):
        print("Moving")
        self.stopped = False

    # Set constant rotation
    def constantRotate(self, speed):
        print("Rotating")
        self.stopped = False

    # Move a certain distance at a speed
    def move(self, speed, distance):
        print("Move " + distance + " at " + speed)
        self.stopped = False

    # Rotate a certain amount at a certain speed
    def rotate(self, speed, degrees):
        print("Rotate " + degrees + " at " + speed)
        self.stopped = False

    # Stop the robot
    def stop(self):
        print("Stop")
        self.stopped = True

class Camera():
    def __init__(self):
        pass

    # Get data from camera
    def getData(self):
        pass

