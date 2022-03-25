from motor import Motor
from serialTeensyToPi import SerialInput
from camera import Camera
import time
import RotateFlipFlop
import Roomba
import Callibration
import StopIfBlue
import RPi.GPIO as GPIO
from buttons import Button
import numpy as np
import cv2
from CameraObject import CameraObject

class Robot():
    def __init__(self, algorithm):
        GPIO.setmode(GPIO.BCM)
        self.left = Motor(12,23)
        self.right = Motor(13,24)
        self.forwardDistanceMod = 3
        self.backwardDistanceMod = 1
        self.rightTurnMod = 1
        self.leftTurnMod = 1
        self.timeCalled = time.time()
        self.timeToKill = 0
        self.constant = False
        self.serial = SerialInput()
        self.camera = Camera(3, False, "main")

        self.algorithm = algorithm
        self.moving = False
        self.leds = {'green':16,
                     'red':20,
                     'yellow':21,
                     'white':18,
                     }
            
    # Callibration
    def getForwardDistanceMod(self):
        return self.forwardDistanceMod
    
    def getBackwardDistanceMod(self):
        return self.backwardDistanceMod
    
    def getRightTurnMod(self):
        return self.rightTurnMod
    
    def getLeftTurnMod(self):
        return self.leftTurnMod
    
    
    # LEDs
    def ledSetup(self):
        for led in self.leds.keys():
            GPIO.setup(self.leds[led], GPIO.OUT)
    
    def ledOn(self, led, alone): # bool alone => only this led should be on.
        if alone:
            self.ledOff()
        GPIO.output(self.leds[led], GPIO.HIGH)
        
    
    def ledOff(self):
        for led in self.leds.keys():
            GPIO.output(self.leds[led], GPIO.LOW)
    
    # Compass
    def getAngle(self):
        self.serial.receiveData()
        return self.serial.getCourse() / 100

    # GPS Data
    def getPosition(self):
        self.serial.receiveData()
        latitude = self.serial.getLatitude()
        longitude = self.serial.getLongitude()
        return latitude, longitude

    # Sensor data
    # Return Dictionary
    def getSensorData(self):
        self.serial.receiveData()
        sensors = {
            'Front': self.serial.getFrontSensorData(),
            'Left': self.serial.getLeftSensorData(),
            'Right': self.serial.getRightSensorData(),
            'FrontRight': self.serial.getFrontRightSensorData(),
            'FrontLeft': self.serial.getFrontLeftSensorData()
        }
        return sensors

    # Camera data, return camera -> splits -> objects
    def getCameraData(self):
        return {self.camera.name: self.camera.getCameraData()}

    def mpsToPercent(self, speedMps):
        return 13 * speedMps

    def dpsToPercent(self, speedDps):
        return speedDps / 6 # do math

    # Tells wether the robot is executing a move
    def isMoving(self):
        return self.moving
    # Set constant speed
    def constantMove(self, speedMps):
        speedPercent = self.mpsToPercent(speedMps)
        self.right.setSpeed(speedPercent)
        self.left.setSpeed(speedPercent)
        self.timeCalled = time.time()
        self.timeToKill = 0
        self.constant = True

    def PID(self, desiredHeading):
        ratio = 0
        
        P = 0
        I = 0
        D = 0

        #tuning variables
        Kp = 0.1
        Ki = 0.1
        Kd = 0.001

        position = 0 #Magnetometer data goes in this variable

        desiredposition = 0 #Whatever heading it is currently at???

        lastError = 0
        error = desiredposition - position

        P = error
        I = I + error
        D = error - lastError
        lastError = error

        motorspeed = P*Kp + I*Ki + D*Kd #PID algo

        position = position + motorspeed #feedback into algo...will need to change

        return ratio

    # Set constant rotation
    def constantRotate(self, speedDps):
        speedPercent = self.dpsToPercent(speedDps)
        self.right.setSpeed(speedPercent*self.rightTurnMod)
        self.left.setSpeed(-speedPercent*self.leftTurnMod)
        self.timeCalled = time.time()
        self.timeToKill = 0
        self.constant = True

    # Move a certain distance at a speed
    def move(self, speedMps, distanceMeters):
        speedPercent = self.mpsToPercent(speedMps)
        seconds = distanceMeters / speedMps
        print('Right speed: %s', speedPercent)
        self.right.setSpeed(speedPercent)
        print('Left speed: %s', speedPercent)
        self.left.setSpeed(speedPercent)
        self.timeCalled = time.time()
        self.timeToKill = seconds
        self.constant = False
        # print("Kill after", self.timeToKill)



    # Rotate a certain amount at a certain speed
    def rotate(self, speedDps, degrees):
        seconds = abs(degrees / speedDps)
        speedPercent = self.dpsToPercent(speedDps)
        # print(speedDps)
        # print(-speedDps)
        self.right.setSpeed(speedPercent)
        self.left.setSpeed(speedPercent)
        self.timeCalled = time.time()
        self.timeToKill = seconds
        self.constant = False

    # Stop the robot
    def stop(self):
        self.left.setSpeed(0)
        self.right.setSpeed(0)
        self.constant = False

    def tick(self):
        t = time.time()
        # print("Time: ", t)
        # print("Called time: ", self.timeCalled)
        self.moving  = self.constant or t - self.timeCalled < self.timeToKill
        if not self.moving:
            self.stop()
        self.algorithm(self, t)



if __name__ == '__main__':
    robot = Robot(StopIfBlue.run)
    robot.ledSetup()
    while(True):
        robot.tick()
