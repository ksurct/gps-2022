
import time
import numpy as np
import cv2
import os
import json

class Camera():

    def __init__(self, splits, show, name):
        self.show = show
        self.cam = cv2.VideoCapture(0)
        self.splitCount = splits
        self.name = name

        # default value
        self.default_red_lower = np.array([136, 100, 111], np.uint8)
        self.default_red_upper = np.array([180, 255, 255], np.uint8)

        # default value
        self.default_yellow_lower = np.array([20, 100, 100], np.uint8)
        self.default_yellow_upper = np.array([30, 255, 255], np.uint8)

        #default value
        self.default_blue_lower = np.array([91, 158, 145], np.uint8)
        self.default_blue_upper = np.array([111, 193, 178], np.uint8)

        if os.path.exists('camera.json'):
            with open('camera.json', 'r') as camera_file:
                try:
                    camera_data = json.load(camera_file)
                    self.red_lower = camera_data['red lower']
                    self.red_upper = camera_data['red upper']

                    self.yellow_lower = camera_data['yellow lower']
                    self.yellow_upper = camera_data['yellow upper']

                    self.blue_lower = camera_data['blue lower']
                    self.blue_upper = camera_data['blue upper']
                except:
                    self.setDefaults()
        else:
            self.setDefaults()
    
    def setDefaults(self):
        self.red_lower = self.default_red_lower 
        self.red_upper = self.default_red_upper 

        self.yellow_lower = self.default_yellow_lower
        self.yellow_upper = self.default_yellow_upper

        self.blue_lower = self.default_blue_lower
        self.blue_upper = self.default_blue_upper

    def end(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def getCameraData(self):
        objects = []
        objectCount = 0
        for i in range(0, self.splitCount):
            objects.append([])
        if(not self.cam.isOpened()):
            return []
        # Reading the video from the
        # cam in image frames
        _, frame = self.cam.read()
        width = frame.shape[1]
        objectCount = 0

        # Convert the frame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Set range for red color and
        # define mask
        red_mask = cv2.inRange(hsvFrame, self.red_lower, self.red_upper)

        # Set range for green color and
        # define mask
        yellow_mask = cv2.inRange(hsvFrame, self.yellow_lower, self.yellow_upper)

        # Set range for blue color and
        # define mask
        blue_mask = cv2.inRange(hsvFrame, self.blue_lower, self.blue_upper)

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

        frame = self.addObject(objects, objectCount, frame, width/self.splitCount, contours, "Red", hsvFrame)

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(yellow_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        frame = self.addObject(objects, objectCount, frame, width/self.splitCount, contours, "Yellow", hsvFrame)

        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(blue_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        frame = self.addObject(objects, objectCount, frame, width/self.splitCount, contours, "Blue", hsvFrame)
        if (self.show):
            width = frame.shape[1]
            for i in range(0, self.splitCount):
                splitWidth = width//self.splitCount
                split = frame[:, int(i*splitWidth):int((i+1)*splitWidth)]
                # Program Termination
                cv2.imshow("Multiple Color Detection in Real-TIme", frame)
                cv2.imshow('split %d' % i, split)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return None
        return objects

    def addObject(self, objects, objectCount, frame, width, contours, color, hsvFrame):
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                split = int(x // (width))
                size = w
                if (x + w > (split+1)*width and split != self.splitCount):
                    size = (split+1)*width - x
                    objects[split+1].append({"hsv": hsvFrame[int(y+h/2), int(x+w/2)], "id": objectCount, "color": color, "x": (split+1)*width, "size": w - size})
                objects[split].append({"hsv": hsvFrame[int(y+h/2), int(x+w/2)], "id": objectCount, "color": color, "x": x, "size": size})
                objectCount+=1
                if (self.show):
                    frame = cv2.rectangle(frame, (x, y),
                                            (x + w, y + h),
                                            (200, 200, 200), 2)

                    cv2.putText(frame, color, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (200, 200, 200))
        return frame

    def tune(self, tolerance):
        dataPoints = []
        while (True):
            data = self.getCameraData()
            print(data)
            count = 0
            for split in data:
                for obj in split:
                    count += 1
                    dataPoints.append(obj["hsv"])
            if (count != 1):
                print("Waiting for 1 item in view")
                # time.sleep(1)
                dataPoints.clear()
            elif len(dataPoints) > 9:
                print("Success")
                h = 0
                s = 0
                v = 0
                for d in dataPoints:
                    h += d[0]
                    s += d[1]
                    v += d[2]
                def maxLim(var, limit):
                    return var if var < limit else limit
                def minLim(var, limit):
                    return var if var > limit else limit
                hL = minLim((h / len(dataPoints)) * (1 - tolerance), 0)
                sL = minLim((s / len(dataPoints)) * (1 - tolerance), 0)
                vL = minLim((v / len(dataPoints)) * (1 - tolerance), 0)
                hH = maxLim((h / len(dataPoints)) * (1 + tolerance), 255)
                sH = maxLim((s / len(dataPoints)) * (1 + tolerance), 255)
                vH = maxLim((v / len(dataPoints)) * (1 + tolerance), 255)
                return (np.array([hL, sL, vL], np.uint8), np.array([hH, sH, vH], np.uint8))

    def tuneBlue(self, tolerance):
        res = self.tune(tolerance)
        self.blue_lower = res[0]
        self.blue_upper = res[1]

        try:
            camera_data = self.openjson()
            camera_data['blue lower'] = self.blue_lower.tolist()
            camera_data['blue upper'] = self.blue_upper.tolist()
        except:
            camera_data = {
                'blue lower': self.blue_lower.tolist(),
                'blue upper': self.blue_upper.tolist()
            }
        finally: 
            with open('camera.json', 'w') as camera_file:
                json.dump(camera_data, camera_file)
            
            print("Using", res, "for blue")

    def tuneRed(self, tolerance):
        res = self.tune(tolerance)
        self.red_lower = res[0]
        self.red_upper = res[1]
        print(self.red_lower)
        print(self.red_upper)
        
        try:
            camera_data = self.openjson()
            camera_data['red lower'] = self.red_lower.tolist()
            camera_data['red upper'] = self.red_upper.tolist()
        except:
            camera_data = {
                'red lower': self.red_lower.tolist(),
                'red upper': self.red_upper.tolist()
            }
        finally:
            with open('camera.json', 'w') as camera_file:
                json.dump(camera_data, camera_file)
            
            print("Using", res, "for red")

    def tuneGreen(self, tolerance):
        res = self.tune(tolerance)
        self.green_lower = res[0]
        self.green_upper = res[1]

        try:
            camera_data = self.openjson()
            camera_data['green lower'] = self.green_lower.tolist()
            camera_data['green upper'] = self.green_upper.tolist()
        except:
            camera_data = {
                'green lower': self.green_lower.tolist(),
                'green upper': self.green_upper.tolist()
            }
        finally:
            with open('camera.json', 'w') as camera_file:
                json.dump(camera_data, camera_file)
            
            print("Using", res, "for green")

    def openjson(self):
        if os.path.exists('camera.json'):
            with open('camera.json') as camera_file:
                return json.load(camera_file)
        else:
             return None

    def createjson(self):
        with open('camera.json', 'w') as camera_file:
            stuff = {
                'red lower': self.red_lower,
                'red upper': self.red_upper,
                'yellow lower': self.yellow_lower,
                'yellow upper': self.yellow_upper,
                'blue lower': self.blue_lower,
                'blue upper': self.blue_upper
            }
            json.dump(stuff, camera_file)

if __name__ == "__main__":
    camera = Camera(3, True, "main")
    # camera.tuneBlue(0.1)
    camera.tuneRed(0.1)
    

