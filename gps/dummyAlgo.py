from multiprocessing.connection import wait
from readline import redisplay
from turtle import delay
import run
import time

mod = 0
state = "MOVE"

def colorCount(split, color):
    for obj in split:
        if (obj["color"] == color):
            return True
    return False

def colorsInSplit(split):
    ret = []
    for obj in split:
        if (not obj["color"] in ret):
            ret.append(obj["color"])
    return ret

def bigestColors(splits, objCount):
    def initCol(col):
        for i in range(objCount):
            col.append({"size": -1, "color": "None"})
    redObjs = []
    blueObjs = []
    yellowObjs = []
    initCol(redObjs)
    initCol(blueObjs)
    initCol(yellowObjs)
    def compare(obj):
        return obj["size"]
    for index, split in enumerate(splits):
        for obj in split:
            obj["split"] = index
            if (obj["color"] == "Red" and obj["size"] > redObjs[0]["size"]):
                redObjs[0] = obj
                redObjs.sort(key=compare)
            elif (obj["color"] == "Blue" and obj["size"] > blueObjs[0]["size"]):
                blueObjs[0] = obj
                yellowObjs.sort(key=compare)
            elif (obj["color"] == "Yellow" and obj["size"] > yellowObjs[0]["size"]):
                yellowObjs[0] = obj
                yellowObjs.sort(key=compare)
    ret = [[],[],[],[],[]]
    for obj in redObjs:
        if (obj["size"] != -1):
            ret[obj["split"]].append(obj)
    for obj in blueObjs:
        if (obj["size"] != -1):
            ret[obj["split"]].append(obj)
    for obj in yellowObjs:
        if (obj["size"] != -1):
            ret[obj["split"]].append(obj)
    return ret

class ReallyDumb():
    def __init__(self) -> None:
        self.state = "INIT"
        self.standardSpeed = 5
        self.standardRotateSpeed = 720
        self.overrodeAction = False
        self.waitCall = None
        self.waitCallTime = None
        self.time = 0
        self.cameraData = [[],[],[],[],[]]
        self.LEFT = 0
        self.FLEFT = 1
        self.FRONT = 2
        self.FRIGHT = 3
        self.RIGHT = 4
        self.delays = {}

        self.periodic = {}
        self.states = {
            "INIT": self.init,
            "CORNER1": self.corner1,
            "YELLOW": self.yellow,
            "CORNER2": self.corner2,
            "CORNER3": self.corner3,
            "FIND_YELLOW": self.findYellow,
            "RAM_YELLOW": self.ramYellow,
            "CORNER4": self.corner4
        }

    def updateCamera(self, robot, time):
        self.cameraData = bigestColors(robot.getCameraData()["main"], 1)

    def printUpdate(self, robot, time):
        sensorData = robot.getSensorData()
        print("Sensors: F:{},R:{},L:{},FR:{},FL:{}".format(
            sensorData["Front"],
            sensorData["Right"],
            sensorData["Left"],
            sensorData["FrontRight"],
            sensorData["FrontLeft"]
        ))

        print("Camera: Left:{},FLeft:{},Front:{},FRight:{},Right:{}".format(
            colorsInSplit(self.cameraData[0]),
            colorsInSplit(self.cameraData[1]),
            colorsInSplit(self.cameraData[2]),
            colorsInSplit(self.cameraData[3]),
            colorsInSplit(self.cameraData[4])
        ))
    
    def overrideCheck(self, robot, time):
        pass
        # sensorData = robot.getSensorData()
        # if (sensorData["Front"] < 0.2 and sensorData["Front"] != -1):
        #     robot.stop()
        #     self.overrodeAction = True

    def init(self, robot, time):
        # self.addPeriodic("status", self.printUpdate, 0.5)
        self.addPeriodic("camera", self.updateCamera, 0.1)
        self.wait(lambda r, t: r.stop(), 2)
        return "FIND_YELLOW"

    def corner1(self, robot, time):
        self.wait(lambda r, t: r.rotate(-720, 15), 5)
        return "CORNER2"

    def corner2(self, robot, time):
        self.wait(lambda r, t: r.move(1, 0.5), 5)
        return "CORNER3"

    def corner3(self, robot, time):
        self.wait(lambda r, t: r.move(-1, 0.5), 5)
        return "CORNER4"

    def corner4(self, robot, time):
        self.wait(lambda r, t: r.move(1, 0.5), 5)
        return "FIND_YELLOW"

    def ramYellow(self, robot, time):
        sensorData = robot.getSensorData()
        if (colorCount(self.cameraData[self.FRONT], "Yellow") == 0):
            return "FIND_YELLOW"
        if (sensorData["Front"] != -1 and sensorData["Front"] < 0.5):
            print("Stop")
            robot.stop()
        else:
            print("Move")
            robot.move(1,1)

    def findYellow(self, robot, time):
        col = "Yellow"
        delayTime = 1
        functionTimeDelay = 1
        if (colorCount(self.cameraData[self.FRONT], col) != 0):
            return "RAM_YELLOW"
            print("Red in front")
        elif (colorCount(self.cameraData[self.FRIGHT], col) != 0):
            print("Red in FRIGHT")
            if (self.delay(delayTime)):
                robot.rotate(self.standardRotateSpeed, 20)
        elif (colorCount(self.cameraData[self.RIGHT], col) != 0):
            print("Red in RIGHT")
            if (self.delay(delayTime)):
                robot.rotate(self.standardRotateSpeed, 40)
        elif (colorCount(self.cameraData[self.FLEFT], col) != 0):
            print("Red in FLEFT")
            if (self.delay(delayTime)):
                robot.rotate(-self.standardRotateSpeed, 20)
        elif (colorCount(self.cameraData[self.LEFT], col) != 0):
            print("Red in LEFT")
            if (self.delay(delayTime)):
                robot.rotate(-self.standardRotateSpeed, 40)
        else:
            if (self.delay(delayTime)):
                robot.rotate(-self.standardRotateSpeed, 40)
        return "FIND_YELLOW"

    def yellow(self, robot, time):
        self.wait(lambda r, t: r.rotate(-720, 180), 5)
        return "CORNER1"

    def wait(self, waitCall, delay):
        self.waitCall = waitCall
        self.waitCallTime = self.time + delay

    def delay(self, delay, name="default"):
        if (not name in self.delays):
            self.delays[name] = self.time + delay
            return False
        else:
            if (self.delays[name] < self.time):
                self.delays.pop(name, None)
                return True
            print("Waiting", self.time, self.delays[name])
            return False
    def runWait(self, robot, time):
        self.waitCall(robot, time)
        self.waitCall = None

    def removePeriodic(self, name):
        self.periodic.pop(name, None)

    def addPeriodic(self, name, function, period):
        if not name in self.periodic:
            self.periodic[name] = {"T":period, "F":function, "PrevTime":self.time}

    def runPeriodic(self, robot, time):
        for key in self.periodic.keys():
            if (self.periodic[key]["PrevTime"] + self.periodic[key]["T"] < time):
                self.periodic[key]["F"](robot, time)
                self.periodic[key]["PrevTime"] = time

    def run(self, robot, time):
        self.time = time
        self.runPeriodic(robot, time)
        self.overrideCheck(robot, time)
        if (self.waitCall != None):
            if (self.waitCallTime < time):
                self.runWait(robot, time)
            else:
                return
        ret = self.states[self.state](robot, time)
        if ret != None and ret != self.state:
            print("Changing to state:", ret)
            self.state = ret

algo = ReallyDumb()

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    algo.run(robot, time)

run.cameraSplits = 5
run.algo = algorithm
run.isSim = False
run.debugCamera = "Internet"
run.run()


