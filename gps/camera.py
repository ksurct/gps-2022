import numpy as np
import cv2

class camera:
    def __init__(self, objectId, color, x, width):
        self.objectId = objectId
        self.color = color
        self.x = x
        self.width = width
        self.video = cv2.VideoCapture(0)


    def __repr__(self):
        return "id:%s color:%s x:%s width:%s" % (self.objectId, self.color, self.x, self.width)

    def createMasks(self):
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


if __name__ == '__main__':
    cam = camera(4,4,4,4)