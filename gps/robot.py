from motor import Motor
from serialTeensyToPi import SerialInput
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
        self.algorithm = algorithm
        self.moving = False
        self.leds = {'green':16,
                     'red':20,
                     'yellow':21,
                     'white':18,
                     }
        self.cam = cv2.VideoCapture(0)
        self.cameraObjects = []
            
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
        
        
        objectCount = 0
        splitCount = 3
    
        if(not self.cam.isOpened()):
            return []
        # Reading the video from the
        # cam in image frames
        _, frame = self.cam.read()
        width = frame.shape[1]
        objects = []
        objectCount = 0

        # Convert the frame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Set range for red color and
        # define mask
        red_lower = np.array([136, 150, 150], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        # Set range for green color and
        # define mask
        yellow_lower = np.array([20, 150, 150], np.uint8)
        yellow_upper = np.array([30, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        # Set range for blue color and
        # define mask
        blue_lower = np.array([94, 150, 150], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between frame and mask determines
        # to detect only that particular color
        kernal = np.ones((5, 5), "uint8")

        # For red color
        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(frame, frame,
                              mask=red_mask)

        # For yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        res_yellow = cv2.bitwise_and(frame, frame,
                                mask=yellow_mask)

        # For blue color
        blue_mask = cv2.dilate(blue_mask, kernal)
        res_blue = cv2.bitwise_and(frame, frame,
                               mask=blue_mask)

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if(x < width//splitCount and (x+w) > width//splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, "Yellow", x, width//splitCount-x))
                    objects.append(CameraObject(objectCount, "Yellow", width//splitCount, x+w-width//splitCount))
                elif(x < 2*width//splitCount and (x+w) > 2*width//splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, "Yellow", x, 2*width//splitCount-x))
                    objects.append(CameraObject(objectCount, "Yellow", 2*width//splitCount, x+w-(2*width//splitCount)))
                else:
                    objects.append(CameraObject(objectCount, "Yellow", x, w))
                frame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

                cv2.putText(frame, "Red", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(yellow_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if(x < width//splitCount and (x+w) > width//splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, "Red", x, width//splitCount-x))
                    objects.append(CameraObject(objectCount, "Red", width//splitCount, x+w-width//splitCount))
                elif(x < 2*width//splitCount and (x+w) > 2*width//splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, "Red", x, 2*width//splitCount-x))
                    objects.append(CameraObject(objectCount, "Red", 2*width//splitCount, x+w-(2*width//splitCount)))
                else:
                    objects.append(CameraObject(objectCount, "Red", x, w))
                frame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (0, 255, 0), 2)

                cv2.putText(frame, "Yellow", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0))

        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if(x < width//splitCount and (x+w) > width//splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, "Blue", x, width//splitCount-x))
                    objects.append(CameraObject(objectCount, "Blue", width//splitCount, x+w-width//splitCount))
                elif(x < 2*width//splitCount and (x+w) > 2*width//splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, "Blue", x, 2*width//splitCount-x))
                    objects.append(CameraObject(objectCount, "Blue", 2*width//splitCount, x+w-(2*width//splitCount)))
                else:
                    objects.append(CameraObject(objectCount, "Blue", x, w))
                objectCount+=1
                frame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 0), 2)

                cv2.putText(frame, "Blue", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))

        width = frame.shape[1]
        left = frame[:, :width//splitCount]
        center = frame[:, width//splitCount:(2*width//splitCount)]
        right = frame[:, (2*width//splitCount):]
        # Program Termination
        cv2.imshow("Multiple Color Detection in Real-TIme", frame)
        cv2.imshow('left', left)
        cv2.imshow('center', center)
        cv2.imshow('right', right)
        self.cameraObjects = objects
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return None
        return objects
    

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
    robot = Robot(StopIfBlue.run)
    robot.ledSetup()
    while(True):
        robot.tick()
