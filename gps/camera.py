
import threading
import time
import numpy as np
import cv2
import os
import json
# import internetCam

class Camera():
    cam = cv2.VideoCapture(0)
    def __init__(self, splits, show, name, internet=False):
        self.show = show
        self.frame = []
        if (show == "Internet"):
            import internetCam
            internetCam.theCam = self
            internetCam.run()
        # self.cam = cv2.VideoCapture(0)
        # self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        self.splitCount = splits
        self.name = name
        self.outFrame = []
        self.defaultAreaRequire = 125
        # internetCam.camera = self
        # internetCam.run()
        self.areaRequired = 125
        # default value
        self.default_red_lower = np.array([136, 100, 111], np.uint8)
        self.default_red_upper = np.array([180, 255, 255], np.uint8)

        # default value
        self.default_yellow_lower = np.array([20, 100, 100], np.uint8)
        self.default_yellow_upper = np.array([30, 255, 255], np.uint8)

        #default value
        #self.default_blue_lower = np.array([91, 158, 145], np.uint8)
        #self.default_blue_upper = np.array([111, 193, 178], np.uint8)
        self.default_blue_lower = np.array([94, 70, 100], np.uint8)
        self.default_blue_upper = np.array([120, 255, 255], np.uint8)

        self.setDefaults()

        if os.path.exists('camera.json'):
            with open('camera.json', 'r') as camera_file:
                try:
                    camera_data = json.load(camera_file)
                    if ("red lower" in camera_data):
                        self.red_lower = np.array(camera_data['red lower'], np.uint8)
                    else:
                        print("Could not find red lower")
                    if ("red upper" in camera_data):
                        self.red_upper = np.array(camera_data['red upper'], np.uint8)
                    else:
                        print("Could not find red upper")
                    if ("yellow lower" in camera_data):
                        self.yellow_lower = np.array(camera_data['yellow lower'], np.uint8)
                    else:
                        print("Could not find yellow lower")
                    if ("yellow upper" in camera_data):
                        self.yellow_upper = np.array(camera_data['yellow upper'], np.uint8)
                    else:
                        print("Could not find yellow upper")
                    if ("blue lower" in camera_data):
                        self.blue_lower = np.array(camera_data['blue lower'], np.uint8)
                    else:
                        print("Could not find blue lower")
                    if ("blue upper" in camera_data):
                        self.blue_upper = np.array(camera_data['blue upper'], np.uint8)
                    else:
                        print("Could not find blue upper")

                    print("Using self.red lower", self.red_lower)
                    print("Using self.red upper", self.red_upper)
                    print("Using self.yellow lower", self.yellow_lower)
                    print("Using self.yellow upper", self.yellow_upper)
                    print("Using self.blue lower", self.blue_lower)
                    print("Using self.blue upper", self.blue_upper)
                except:
                    print("Failed to load values")
        else:
            self.setDefaults()
        # self.setDefaults()

    def getFrame(self):
        if (len(self.outFrame) != 0):
            return self.outFrame
        return self.frame

    def setDefaults(self):
        print("Setting defaults")
        self.red_lower = self.default_red_lower 
        self.red_upper = self.default_red_upper 

        self.yellow_lower = self.default_yellow_lower
        self.yellow_upper = self.default_yellow_upper

        self.blue_lower = self.default_blue_lower
        self.blue_upper = self.default_blue_upper

    def end(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def tick(self):
        _, self.frame = self.cam.read()

    def getCameraData(self):
        objects = []
        objectCount = 0
        for i in range(0, self.splitCount):
            objects.append([])
        if(not self.cam.isOpened()):
            return []
        # Reading the video from the
        # cam in image frames
        #_, frame = self.cam.read()
        frame = self.frame
        if (len(frame) == 0):
            #self.tick()
            _, frame = self.cam.read()
        # frame = frame[int(len(frame)*0.5):int(len(frame)*0.65)]
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
        if (self.show == True):
            width = frame.shape[1]
            for i in range(0, self.splitCount):
                splitWidth = width//self.splitCount
                # split = frame[:, int(i*splitWidth):int((i+1)*splitWidth)]
                # Program Termination
                cv2.imshow("Multiple Color Detection in Real-TIme", frame)
                # cv2.imshow('split %d' % i, split)
        elif(self.show == "Internet"):
            self.outFrame = frame
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return None
        return objects

    def addObject(self, objects, objectCount, frame, width, contours, color, hsvFrame):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        cutoff = frameHeight * 0.5

        cv2.line(frame, (0, cutoff), (frameWidth, cutoff), (200, 0, 0))

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > self.areaRequired):
                x, y, w, h = cv2.boundingRect(contour)
                split = int(x // (width))
                size = w
                # check if in dimension tolerance and bottom is below certain point
                if (w / h < 1 and y + h > cutoff):
                    if (x + w > (split+1)*width and split != self.splitCount and w / h < 1 and y + h > frame.shape[0] * 0.5):
                        size = (split+1)*width - x
                        objects[split+1].append({"hsv": hsvFrame[int(y+h/2), int(x+w/2)], "id": objectCount, "color": color, "x": (split+1)*width, "size": (w - size)/width})
                    objects[split].append({"hsv": hsvFrame[int(y+h/2), int(x+w/2)], "id": objectCount, "color": color, "x": x, "size": size/width})
                    objectCount+=1
                    if (self.show):
                        frame = cv2.rectangle(frame, (x, y),
                                                (x + w, y + h),
                                                (200, 200, 200), 2)

                        cv2.putText(frame, color, (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.0, (200, 200, 200))
        return frame

    def tune(self, tolerance, color):
        dataPoints = []
        while (True):
            data = self.getCameraData()
            print(data)
            count = 0
            largestSize = 0
            largest = None
            for split in data:
                for obj in split:
                    if (obj["color"] == color):
                        count += 1
                        if (largestSize < obj["size"]):
                            largest = obj
            if (largest != None):
                dataPoints.append(largest["hsv"])
            if (count < 1):
                print("Waiting for 1 item in view")
                # time.sleep(1)
                dataPoints.clear()
            elif len(dataPoints) > 60:
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


    def dumTune(self, tolerance, color):
        dataPoints = []
        count = 0
        self.tick()
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        x = len(self.hsvFrame) // 2
        y = len(self.hsvFrame[0]) // 2
        turnOff = False
        def run():
            while (not turnOff):
                self.tick()
                col = cv2.cvtColor(np.array([[self.hsvFrame[x][y]]], np.uint8), cv2.COLOR_HSV2BGR)
                self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                self.outFrame = cv2.rectangle(self.frame, (y - 5, x - 5),
                            (y + 5, x + 5),
                            (0,0,0), 2)
                self.outFrame = cv2.rectangle(self.outFrame, (y - 100, x - 100),
                            (y + 100, x + 100),
                            col[0][0].tolist(), 2)
        t = threading.Thread(target=run)
        print("2")
        t.start()
        print("1")
        total = 5
        while(True):
            if (input("Count %d / %d, Is this Good? " % (count + 1, total)).upper() == "Y"):
                count += 1
                center = self.hsvFrame[x][y]
                dataPoints.append(center)
            if (count >= total):
                turnOff = True
                t.join()
                break

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
        sL = minLim((s / len(dataPoints)) * (1 - tolerance*3), 0)
        vL = minLim((v / len(dataPoints)) * (1 - tolerance), 0)
        hH = maxLim((h / len(dataPoints)) * (1 + tolerance), 255)
        sH = maxLim((s / len(dataPoints)) * (1 + tolerance*3), 255)
        vH = maxLim((v / len(dataPoints)) * (1 + tolerance), 255)
        return (np.array([hL, sL, vL], np.uint8), np.array([hH, sH, vH], np.uint8))
        

    def tuneBlue(self, tolerance):
        self.areaRequired = 200
        self.blue_lower = self.default_blue_lower
        self.blue_upper = self.default_blue_upper
        res = self.dumTune(tolerance, "Blue")
        self.blue_lower = res[0]
        self.blue_upper = res[1]
        self.areaRequired = self.defaultAreaRequire
        return (self.blue_lower.tolist(),
            self.blue_upper.tolist())

    def tuneRed(self, tolerance):
        self.areaRequired = 200
        self.red_lower = self.default_red_lower
        self.red_upper = self.default_red_upper
        res = self.dumTune(tolerance, "Red")
        self.red_lower = res[0]
        self.red_upper = res[1]
        print(self.red_lower)
        print(self.red_upper)
        self.areaRequired = self.defaultAreaRequire
        return (self.red_lower.tolist(),
            self.red_upper.tolist())

    def tuneYellow(self, tolerance):
        self.areaRequired = 200
        self.yellow_lower = self.default_yellow_lower
        self.yellow_upper = self.default_yellow_upper
        res = self.dumTune(tolerance, "Yellow")
        self.yellow_lower = res[0]
        self.yellow_upper = res[1]
        self.areaRequired = self.defaultAreaRequire
        return (self.yellow_lower.tolist(),
            self.yellow_upper.tolist())

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

    def __del__(self):
        if (self.show == "Internet"):
            import internetCam
            internetCam.exit()

if __name__ == "__main__":
    yn1 = input("Tune? ")
    yn2 = input("InternetCam? ")
    show = True
    if (yn2 == "y"):
        show = "Internet"
    if (yn1 == "y"):
        cameraTune = {}
        camera = Camera(1, show, "main")
        try:
            tol = float(input("Tuning red, tolerance = "))
            res = camera.tuneRed(tol)
            cameraTune["red lower"] = res[0]
            cameraTune["red upper"] = res[1]
            tol = float(input("Tuning yellow, tolerance = "))
            time.sleep(2)
            res = camera.tuneYellow(tol)
            cameraTune["yellow lower"] = res[0]
            cameraTune["yellow upper"] = res[1]
            tol = float(input("Tuning blue, tolerance = "))
            time.sleep(2)
            res = camera.tuneBlue(tol)
            cameraTune["blue lower"] = res[0]
            cameraTune["blue upper"] = res[1]
        except:
            pass
        with open('camera.json', 'w') as camera_file:
            json.dump(cameraTune, camera_file)
        exit()
    else:
        camera = Camera(3, show, "main")

    while(True):
        objs = camera.getCameraData()
        if(objs == None):
            break
        else:
            for split in objs:
                for object in split:
                    pass
                    # print(object["hsv"])
            # print(objs)

