from motor import Motor
from serialTeensyToPi import SerialInput
import time
import RotateFlipFlop
import Roomba
import Callibration
import RPi.GPIO as GPIO
from buttons import Button

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
        self.algorithm = algorithm
        self.moving = False
        self.leds = {'green':16,
                     'red':20,
                     'yellow':21,
                     'white':18,
                     }
        self.buttonPins = [11, 25, 8, 7]
        self.buttons = []
        self.buttonsPopulated = False # wether or not buttons have already been assigned to pins
            
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
    
    # Buttons
    def buttonsSetup(self, functions):
        print('Button pins:')
        if len(functions) < 5:
            for i in range(len(functions)):
                print(self.buttonPins[i])
                self.buttons.append(Button(self, self.buttonPins[i], functions[i]))
            self.buttonsPopulated = True
        else:
            print('Too many functions!')
    
    def buttonsPopulated(self):
        return self.buttonsPopulated
    
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
        pass

    def mpsToPercent(self, speedMps):
        return 4 / 0.78 * speedMps

    def dpsToPercent(self, speedRps):
        return speedRps # do math

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



    # Set constant rotation
    def constantRotate(self, speedDps):
        speedPercent = self.dpsToPercent(speedDps)
        self.right.setSpeed(-speedPercent*self.rightTurnMod)
        self.left.setSpeed(speedPercent*self.leftTurnMod)
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
        self.left.setSpeed(-speedPercent)
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
    from RPi import GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    robot = Robot(Roomba.run)
    robot.ledSetup()
    while(True):
        robot.tick()
