from cmath import pi
from motor import Motor
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
from simple_pid import PID

class Robot():
    def __init__(self, algorithm):
        GPIO.setmode(GPIO.BCM)
        self.left = Motor(12,23, 0.9)
        self.right = Motor(13,24, 1.1)
        self.speed = 0
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
        self.forward = False
        self.leds = {'green':16,
                     'red':20,
                     'yellow':21,
                     'white':18,
                     }
        self.kp = 1
        self.ki = 1
        self.kd = 1
        self.pid = PID(Kp=self.kp, Ki=self.ki, Kd=self.kd, setpoint=0)
        self.pid.output_limits = (-10, 10)
        self.pid.auto_mode = True
        self.axilLength = .325 # meters
        self.wheelDiameter = 0.086
    
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

    def isNotMoving(self):
        return not self.moving

    # Set constant speed
    def constantMove(self, speedMps):
        self.setRightMps(speedMps)
        self.setLeftMps(speedMps)
        self.timeCalled = time.time()
        self.timeToKill = 0
        self.constant = True

    # Set constant rotation
    def constantRotate(self, speedDps):
        circumferenceTurn = self.axilLength * pi
        mpd = circumferenceTurn / 360
        speedMps = speedDps * mpd
        self.setLeftMps(speedMps)
        self.setRightMps(-speedMps)

        self.timeCalled = time.time()
        self.timeToKill = 0
        self.constant = True

    # Move a certain distance at a speed
    def move(self, speedMps, distanceMeters):
        seconds = distanceMeters / speedMps
        self.constantMove(speedMps)
        self.timeCalled = time.time()
        self.timeToKill = seconds
        self.constant = False

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
        ω = speed * 2 * pi / (2*radius*pi)
        Vr = ω* (radius + self.axilLength/2)
        Vl = ω* (radius - self.axilLength/2)
        print("VL = ", Vl)
        print("Vr = ", Vr)
        self.setLeftMps(Vl)
        self.setRightMps(Vr)
        self.timeCalled = time.time()
        self.constant = True

    def arcMove(self, speed, radius, distance):
        # Gravity at center of circle = v^2 / r
        # angular velocity = (360 / circumference) * v
        self.constantArcMove(speed, radius)
        self.timeToKill = distance / abs(speed)
        self.timeCalled = time.time()
        self.constant = False

    # Rotate a certain amount at a certain speed
    def rotate(self, speedDps, degrees):
        self.constantRotate(speedDps)
        seconds = abs(degrees / speedDps)
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
        self.moving  = self.constant or t - self.timeCalled < self.timeToKill
        if not self.moving:
            self.stop()
        self.algorithm(self, t)

if __name__ == '__main__':
    robot = Robot(Roomba.run)
    robot.ledSetup()
    while(True):
        robot.tick()
