# Python code for Multiple Color Detection


import numpy as np
import cv2
from CameraObject import CameraObject

# Capturing video through cam
cam = cv2.VideoCapture(0)

# Array of objects
objects = []
objectCount = 0

splitCount = 3

def getCameraData():
    if(not cam.isOpened()):
        return []
    # Reading the video from the
    # cam in image frames
    _, frame = cam.read()
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
    red_lower = np.array([136, 100, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and
    # define mask
    yellow_lower = np.array([20, 100, 100], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([94, 80, 100], np.uint8)
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
    print([objects])
    if cv2.waitKey(10) & 0xFF == ord('q'):
        return None
    return []

if __name__ == "__main__":
    while(True):
        if(getCameraData() == None):
            break

cam.release()
cv2.destroyAllWindows()