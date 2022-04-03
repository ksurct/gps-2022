from multiprocessing.connection import wait
from readline import redisplay
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

def bigestColors(splits):
    redSplit = -1
    redObj = {"size":-1}
    blueObj = {"size":-1}
    blueSplit = -1
    yellowObj = {"size":-1}
    yellowSplit = -1
    for index, split in enumerate(splits):
        for obj in split:
            if (obj["color"] == "Red" and obj["size"] > redObj["size"]):
                redObj = obj
                redSplit = index
            elif (obj["color"] == "Blue" and obj["size"] > blueObj["size"]):
                blueObj = obj
                blueSplit = index
            elif (obj["color"] == "Yellow" and obj["size"] > yellowObj["size"]):
                yellowObj = obj
                yellowSplit = index
    ret = [[],[],[],[],[]]
    if (redSplit != -1):
        ret[redSplit].append(redObj)
    if (yellowSplit != -1):
        ret[yellowSplit].append(yellowObj)
    if (blueSplit != -1):
        ret[blueSplit].append(blueObj)
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

        self.periodic = {}
        self.states = {
            "INIT": self.init,
            "CORNER1": self.corner1,
            "YELLOW": self.yellow,
            "CORNER2": self.corner2,
            "CORNER3": self.corner3,
            "RED": self.red,
            "CORNER4": self.corner4
        }

    def updateCamera(self, robot, time):
        self.cameraData = bigestColors(robot.getCameraData()["main"])

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
        sensorData = robot.getSensorData()
        if (sensorData["Front"] < 0.25 and sensorData["Front"] != -1):
            robot.stop()
            self.overrodeAction = True

    def init(self, robot, time):
        # self.addPeriodic("status", self.printUpdate, 0.5)
        self.addPeriodic("camera", self.updateCamera, 0.1)
        self.wait(lambda r, t: r.rotate(720, 15), 5)
        return "RED"

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
        return "RED"

    def red(self, robot, time):
        if (colorCount(self.cameraData[self.FRONT], "Blue") != 0):
            print("Red in front")
        elif (colorCount(self.cameraData[self.FRIGHT], "Blue") != 0):
            print("Red in FRIGHT")
            self.wait(lambda r, t: robot.rotate(self.standardRotateSpeed, 20), 1.5)
        elif (colorCount(self.cameraData[self.RIGHT], "Blue") != 0):
            print("Red in RIGHT")
            self.wait(lambda r, t: robot.rotate(self.standardRotateSpeed, 40), 1.5)
        elif (colorCount(self.cameraData[self.FLEFT], "Blue") != 0):
            print("Red in FLEFT")
            self.wait(lambda r, t: robot.rotate(-self.standardRotateSpeed, 20), 1.5)
        elif (colorCount(self.cameraData[self.LEFT], "Blue") != 0):
            print("Red in LEFT")
            self.wait(lambda r, t: robot.rotate(-self.standardRotateSpeed, 40), 1.5)
        else:
            self.wait(lambda r, t: robot.rotate(-self.standardRotateSpeed, 40), 1.5)

        return "RED"

    def yellow(self, robot, time):
        self.wait(lambda r, t: r.rotate(-720, 180), 5)
        return "CORNER1"

    def wait(self, waitCall, delay):
        self.waitCall = waitCall
        self.waitCallTime = self.time + delay

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


