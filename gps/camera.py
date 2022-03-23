import numpy as np
import cv2

class camera:
    def __init__(self, splitCount):
        self.video = cv2.VideoCapture(0)
        _, self.frame = self.video.read()
        self.width = self.frame.shape[1]
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.kernal = np.ones((5,5), 'uint8')
        self.splitCount = splitCount
        self.createMasks()


    def __repr__(self):
        return "id:%s color:%s x:%s width:%s" % (self.objectId, self.color, self.x, self.width)

    def createMasks(self):
        red_lower = np.array([136, 100, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        self.red_mask = cv2.inRange(self.hsvFrame, red_lower, red_upper)
        self.red_mask = cv2.dilate(self.red_mask, self.kernal)

        # Set range for green color and
        # define mask
        yellow_lower = np.array([20, 100, 100], np.uint8)
        yellow_upper = np.array([30, 255, 255], np.uint8)
        self.yellow_mask = cv2.inRange(self.hsvFrame, yellow_lower, yellow_upper)
        self.yellow_mask = cv2.dilate(self.yellow_mask, self.kernal)

        # Set range for blue color and
        # define mask
        blue_lower = np.array([94, 80, 100], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        self.blue_mask = cv2.inRange(self.hsvFrame, blue_lower, blue_upper)
        self.blue_mask = cv2.dilate(self.blue_mask, self.kernal)

    def something(self):
        objects = []
        objectCount = 0
        contours, hierarchy = cv2.findContours(self.red_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if(x < self.width//self.splitCount and (x+w) > self.width//self.splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, "Yellow", x, self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, "Yellow", self.width//self.splitCount, x+w-self.width//self.splitCount))
                elif(x < 2*self.width//self.splitCount and (x+w) > 2*self.width//self.splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, "Yellow", x, 2*self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, "Yellow", 2*self.width//self.splitCount, x+w-(2*self.width//self.splitCount)))
                else:
                    objects.append(CameraObject(objectCount, "Yellow", x, w))
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (0, 0, 255), 2)

                cv2.putText(frame, "Red", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(self.yellow_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if(x < self.width//self.splitCount and (x+w) > self.width//self.splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, "Red", x, self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, "Red", self.width//self.splitCount, x+w-self.width//self.splitCount))
                elif(x < 2*self.width//self.splitCount and (x+w) > 2*self.width//self.splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, "Red", x, 2*self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, "Red", 2*self.width//self.splitCount, x+w-(2*self.width//self.splitCount)))
                else:
                    objects.append(CameraObject(objectCount, "Red", x, w))
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (0, 255, 0), 2)

                cv2.putText(frame, "Yellow", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0, 255, 0))

        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(self.blue_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if(x < self.width//self.splitCount and (x+w) > self.width//self.splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, "Blue", x, self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, "Blue", self.width//self.splitCount, x+w-self.width//self.splitCount))
                elif(x < 2*self.width//self.splitCount and (x+w) > 2*self.width//self.splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, "Blue", x, 2*self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, "Blue", 2*self.width//self.splitCount, x+w-(2*self.width//self.splitCount)))
                else:
                    objects.append(CameraObject(objectCount, "Blue", x, w))
                objectCount+=1
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (255, 0, 0), 2)

                cv2.putText(frame, "Blue", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (255, 0, 0))

    def contour(self, color: str):
        objectCount = 0
        objects = []
        if color == 'Red':
            mask = self.red_mask
        elif color == 'Yellow':
            mask = self.yellow_mask
        elif color == 'Blue':
            mask = self.blue_mask
        else:
            print('Not a valid color')
            return []
        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                if x < (self.width // self.splitCount) and (x+w) > (self.width // self.splitCount): # object split into left and center
                    objects.append(CameraObject(objectCount, color, x, self.width // self.splitCount-x))
                    objects.append(CameraObject(objectCount, color, self.width//self.splitCount, x+w-self.width//self.splitCount))
                elif(x < 2*self.width//self.splitCount and (x+w) > 2*self.width//self.splitCount): # object split into center and right
                    objects.append(CameraObject(objectCount, color, x, 2*self.width//self.splitCount-x))
                    objects.append(CameraObject(objectCount, color, 2*self.width//self.splitCount, x+w-(2*self.width//self.splitCount)))
                else:
                    objects.append(CameraObject(objectCount, color, x, w))
                objectCount+=1
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (255, 0, 0), 2)

                cv2.putText(frame, color, (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (255, 0, 0))
        return objects


class CameraObject():
    
    def __init__(self, objectId, color, x, width):
        self.objectId = objectId
        self.color = color
        self.x = x
        self.width = width
        
    def __repr__(self):
        return "id:%s color:%s x:%s width:%s" % (self.objectId, self.color, self.x, self.width)

if __name__ == '__main__':
    cam = camera(4)
    cam.contour('Blue')
