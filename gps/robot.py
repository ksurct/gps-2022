from motor import Motor

class Robot():
    def __init__(self):
        pass

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
        pass

    # Set constant rotation
    def constantRotate(self, speed):
        pass

    # Move a certain distance at a speed
    def move(self, speed, distance):
        pass

    # Rotate a certain amount at a certain speed
    def rotate(self, speed, degrees):
        pass

    # Stop the robot
    def stop(self):
        pass

class Camera():
    def __init__(self):
        pass

    # Get data from camera
    def getData(self):
        pass

