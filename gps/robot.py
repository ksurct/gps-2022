from cmath import pi
from motor import Motor
import math
from serialTeensyToPi import SerialInput
from camera import Camera
import time
import RotateFlipFlop
import Callibration
import StopIfBlue
import RPi.GPIO as GPIO
from buttons import Button
import numpy as np
import cv2
from CameraObject import CameraObject

class Robot():
    def __init__(self, algorithm, camera):
        GPIO.setmode(GPIO.BCM)
        self.left = Motor(12,23, 0.9)
        self.right = Motor(13,24, 1.1)
        self.speed = 0
        self.forwardDistanceMod = 3
        self.backwardDistanceMod = 1
        self.rightTurnMod = 1
        self.leftTurnMod = 1
        self.timeToKill = 0
        self.time = 0
        self.constant = False
        self.serial = SerialInput()
        self.camera = camera

        self.algorithm = algorithm
        self.moving = False
        self.forward = False
        self.leds = {'green':16,
                     'red':20,
                     'yellow':21,
                     'white':18,
                     }
        self.kp = 1
        self.ki = 1
        self.kd = 1
        self.axilLength = .325 # meters
        self.wheelDiameter = 0.086

        self.initialPosition = (0,0)
        self.initialAngle = 0

    def latLongDistance(self,lat1,lon1,lat2,lon2):
        R = 6371 # Radius of the earth in km
        dLat = math.radians(lat2-lat1)
        dLon = math.radians(lon2-lon1)
        a = (
            math.sin(dLat/2) * math.sin(dLat/2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dLon/2) * math.sin(dLon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c # Distance in km
        return d

    def initAngle(self):
        self.initialAngle = 0
        for i in range(0,10):
            self.initialAngle += self.getAngle()
        self.initAngle /= 10

    def convertToRelativeCoords(self, pos):
        return (
            math.cos(math.radians(self.initialAngle)) * pos[0] + math.sin(math.radians(self.initialAngle)) * pos[1],
            math.sin(math.radians(self.initialAngle)) * pos[0] - math.cos(math.radians(self.initialAngle)) * pos[1]
        )

    def initPosition(self):
        while (self.initialPosition[0] == 0):
            self.serial.receiveData()
            self.initialPosition = (self.serial.getLatitude(), self.serial.getLongitude())
            print("Waiting for GPS")
            time.sleep(0.1)

    # Callibration
    def getForwardDistanceMod(self):
        return self.forwardDistanceMod

    def getBackwardDistanceMod(self):
        return self.backwardDistanceMod

    def getRightTurnMod(self):
        return self.rightTurnMod

    def getLeftTurnMod(self):
        return self.leftTurnMod

    def setLeftMps(self, mps):
        maxMotorRpm = 10500
        maxMotorRps = 10500 / 60
        maxOutputRps = maxMotorRps / 5 # gear ratio
        maxMps = maxOutputRps * self.wheelDiameter * pi
        # y = mx + b
        self.left.setSpeed((mps/maxMps) * 100)

    def setRightMps(self, mps):
        maxMotorRps = 10500 / 60
        maxOutputRps = maxMotorRps / 5 # gear ratio
        maxMps = maxOutputRps * self.wheelDiameter * pi
        # y = mx + b
        self.right.setSpeed((mps/maxMps) * 100)

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
        return 0
        self.serial.receiveData()
        return self.serial.getCourse() / 100

    # GPS Data
    def getPosition(self):
        self.serial.receiveData()
        latitude = self.serial.getLatitude()
        longitude = self.serial.getLongitude()
        metersX = self.latLongDistance(self.initialPosition[0], self.initialPosition[1], self.initialPosition[0], longitude)
        metersY = self.latLongDistance(self.initialPosition[0], self.initialPosition[1], latitude, self.initialPosition[1])
        metersX, metersY = self.convertToRelativeCoords((metersX, metersY))

        return metersX, metersY

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

    def isNotMoving(self):
        return not self.moving

    # Set constant speed
    def constantMove(self, speedMps):
        self.setRightMps(speedMps)
        self.setLeftMps(speedMps)
        self.timeToKill = -1
        self.moving = True


    # Set constant rotation
    def constantRotate(self, speedDps):
        circumferenceTurn = self.axilLength * pi
        mpd = circumferenceTurn / 360
        speedMps = speedDps * mpd
        self.setLeftMps(speedMps)
        self.setRightMps(-speedMps)
        self.moving = True
        self.timeToKill = -1

    # Move a certain distance at a speed
    def move(self, speedMps, distanceMeters):
        seconds = abs(distanceMeters / speedMps)
        self.constantMove(speedMps)
        self.timeToKill = self.time + seconds
        self.moving = True

    def motorPID(self):
        pass
        # output = self.pid(self.serial.getAccelY())
        # if output < 0:
        #     self.left.setSpeed(self.speed + output)
        #     self.right.setSpeed(self.speed)
        # elif output > 0:
        #     self.right.setSpeed(self.speed - output)
        #     self.left.setSpeed(self.speed)

    def constantArcMove(self, speed, radius):
        radius = radius * 0.25
        ω = speed * 2 * pi / (2*radius*pi)
        Vl = ω* (radius + self.axilLength/2)
        Vr = ω* (radius - self.axilLength/2)
        self.setLeftMps(Vl)
        self.setRightMps(Vr)
        self.moving = True

    def arcMove(self, speed, radius, distance):
        # Gravity at center of circle = v^2 / r
        # angular velocity = (360 / circumference) * v
        self.constantArcMove(speed, radius)
        self.timeToKill = self.time + distance / abs(speed)
        self.moving = True

    # Rotate a certain amount at a certain speed
    def rotate(self, speedDps, degrees):
        self.constantRotate(speedDps)
        speedDps = speedDps *  220 / 690
        seconds = abs(degrees / speedDps)
        self.moving = True
        self.timeToKill = self.time + seconds

    def initAngle(self):
        self.serial.receiveData()
        self.angleOff = self.serial.getMag()

    def getAngle(self):
        self.serial.receiveData()
        #preangle = self.serial.getMag()
        #angle = preangle + self.angleOff
        #if angle > 180:
        #    angle -= 360
        #if angle < -180:
        #    angle += 360
        #return angle

        
    # Stop the robot
    def stop(self):
        self.left.setSpeed(0)
        self.right.setSpeed(0)
        self.moving = False
        self.timeToKill = -1

    def tick(self):
        self.time = time.time()
        if (self.moving and self.timeToKill != -1):
            if (self.time > self.timeToKill):
                self.stop()
        self.algorithm(self, self.time)

if __name__ == '__main__':
    robot = Robot(Roomba.run)
    robot.ledSetup()
    while(True):
        robot.tick()
