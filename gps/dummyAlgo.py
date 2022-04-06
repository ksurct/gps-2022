
import run
import time

mod = 0
state = "MOVE"
#sensor check
def sCheck(value, distance):
    return value < distance and value != -1

def anyColorOf(data, col):
    for split in data:
        for obj in split:
            if (obj["color"] == col):
                return True
    return False

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
        self.standardSpeed = 1
        self.standardRotateSpeed = 720
        self.overrodeAction = False
        self.waitQueue = []
        self.currentWait = None
        self.vars = {}
        self.time = 0
        self.cameraData = [[],[],[],[],[]]
        self.LEFT = 0
        self.FLEFT = 1
        self.FRONT = 2
        self.FRIGHT = 3
        self.RIGHT = 4
        self.delays = {}
        self.objCount = 1
        self.sdt = 1

        self.periodic = {}
        self.states = {
            "INIT": self.init,
            "CORNER1": self.corner1,
            "YELLOW": self.yellow,
            "CORNER2": self.corner2,
            "CORNER3": self.corner3,
            # "FIND_YELLOW": self.findYellow,
            # "RAM_YELLOW": self.ramYellow,
            "FIND_RED": self.findRed,
            "LEFT_RED": self.leftRed,
            "RIGHT_RED": self.rightRed,
            "CORNER4": self.corner4,
            "STITCH": self.stitch,
            "STITCH2": self.stitch2
        }

    def updateCamera(self, robot, time):
        self.cameraData = bigestColors(robot.getCameraData()["main"], self.objCount)

    def printUpdate(self, robot, time):
        # sensorData = robot.getSensorData()
        # print("Sensors: F:{},R:{},L:{},FR:{},FL:{}".format(
        #     sensorData["Front"],
        #     sensorData["Right"],
        #     sensorData["Left"],
        #     sensorData["FrontRight"],
        #     sensorData["FrontLeft"]
        # ))

        # print("Camera: Left:{},FLeft:{},Front:{},FRight:{},Right:{}".format(
        #     colorsInSplit(self.cameraData[0]),
        #     colorsInSplit(self.cameraData[1]),
        #     colorsInSplit(self.cameraData[2]),
        #     colorsInSplit(self.cameraData[3]),
        #     colorsInSplit(self.cameraData[4])
        # ))

        print("Angle: " + str(robot.getAngle()))
    
    def overrideCheck(self, robot, time):
        sensorData = robot.getSensorData()
        if (sensorData["Front"] < 0.2 and sensorData["Front"] != -1):
            robot.stop()
            self.overrodeAction = True

    def leftRed(self, robot, time):
        self.goAround(robot, "Red", -1)

    def rightRed(self, robot, time):
        self.goAround(robot, "Red", 1)

    def findRed(self, robot, time):
        self.objCount = 2
        data = robot.getSensorData()
        if (sCheck(data["Front"], 0.5)):
            print("Found")
            robot.stop()
            if (colorCount(self.cameraData[self.LEFT], "Red")):
                return "LEFT_RED"
            elif (colorCount(self.cameraData[self.RIGHT], "Red")):
                return "RIGHT_RED"
            elif (colorCount(self.cameraData[self.FRIGHT], "Red")):
                return "LEFT_RED"
            elif (colorCount(self.cameraData[self.FLEFT], "Red")):
                return "RIGHT_RED"
        elif (self.findColor(robot, time, "Red")):
            robot.move(self.standardSpeed,1)

    def init(self, robot, time):
        self.addPeriodic("camera", self.updateCamera, 0.1)                          
        # return "FIND_RED"
        self.addPeriodic("status", self.printUpdate, 0.2)
        delayTime = 0.25
        robot.initAngle()
        # if(self.delay(delayTime)):
        #     robot.rotate(-self.standardRotateSpeed, 40)
        robot.move(1,2)
        #self.wait(lambda r, t: r.time, 5)
        if (self.delay(1, "Something")):
            print("FIRST STATE")
            return "CORNER1"

    def corner1(self, robot, time):
        # self.roundAndRound(robot, "Blue")
        ret = self.goAround(robot, "Blue", 1)
        if (robot.getAngle() > 120 and ret == "move"):
            print("MAG HAS WORKED")
            return "STITCH"
        return "CORNER1"

    def corner2(self, robot, time):
        status = self.goAround(robot, "Yellow", -1)
        angle = robot.getAngle()
        if(angle <= 60 and angle > 0 and status == "move"):
            return "STITCH2"

    def corner3(self, robot, time):
        self.goAround(robot, "Blue", 1)
        # if(robot.getAngle() <= -170 and robot.getAngle() >= 170):
        #     return "CORNER4"

    def corner4(self, robot, time):
        self.wait(lambda r, t: r.move(1, 0.5), 5)
        return "FIND_YELLOW"
    
    def stitch(self, robot, time):
        col = "Yellow"
        angle = robot.getAngle()
        if(not anyColorOf(self.cameraData, col)):
            robot.move(1, 0.5)
        else:
            return "CORNER2"
    
    def stitch2(self, robot, time):
        col = "Blue"
        angle = robot.getAngle()
        if(not anyColorOf(self.cameraData, col)):
            robot.move(1, 0.5)
        else:
            return "CORNER3"

    def ramColor(self, robot, time, color):
        sensorData = robot.getSensorData()
        if (colorCount(self.cameraData[self.FRONT], color) == 0):
            return "Lost"
        if (sensorData["Front"] != -1 and sensorData["Front"] < 0.5):
            robot.stop()
            return "Done"
        else:
            robot.constantMove(1)
            return "Move"

    def findColor(self, robot, time, col):
        delayTime = 1
        if (colorCount(self.cameraData[self.FRONT], col) != 0):
            return True
        elif (colorCount(self.cameraData[self.FRIGHT], col) != 0):
            if (self.delay(delayTime)):
                robot.rotate(self.standardRotateSpeed, 20)
        elif (colorCount(self.cameraData[self.RIGHT], col) != 0):
            if (self.delay(delayTime)):
                robot.rotate(self.standardRotateSpeed, 40)
        elif (colorCount(self.cameraData[self.FLEFT], col) != 0):
            if (self.delay(delayTime)):
                robot.rotate(-self.standardRotateSpeed, 20)
        elif (colorCount(self.cameraData[self.LEFT], col) != 0):
            if (self.delay(delayTime)):
                robot.rotate(-self.standardRotateSpeed, 40)
        else:
            if (self.delay(delayTime)):
                robot.rotate(-self.standardRotateSpeed, 40)
        return False

    def yellow(self, robot, time):
        self.wait(lambda r, t: r.rotate(-720, 180), 5)
        return "CORNER1"

    def wait(self, waitCall, delay):
        self.waitQueue.append((waitCall, delay))

    def delay(self, delay, name="default"):
        delay = self.sdt * delay
        if (not name in self.delays):
            self.delays[name] = self.time + delay
            return False
        else:
            if (self.delays[name] <= self.time):
                self.delays.pop(name, None)
                return True
            return False

    def runWait(self, robot, time):
        if (self.currentWait == None):
            if (len(self.waitQueue) != 0):
                self.currentWait = self.waitQueue.pop(0)
                self.currentWait[0](robot, time)
                return True
            return False
        elif (self.delay(self.currentWait[1], "waitQueue")):
            self.currentWait = None
            return False
        return True

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
        if (self.runWait(robot, time)):
            return
        ret = self.states[self.state](robot, time)
        if ret != None and ret != self.state:
            print("Changing to state:", ret)
            self.state = ret
    
    def roundAndRound(self, robot, col):
        if(robot.isNotMoving() and self.delay(0.5)):
            if (colorCount(self.cameraData[self.FRONT], col) != 0 or colorCount(self.cameraData[self.FRIGHT], col) != 0):
                robot.rotate(-self.standardRotateSpeed, 15)
                # if(self.delay(delayTime)):
                #     robot.move(2, 1)
            elif (colorCount(self.cameraData[self.RIGHT], col) == 0):
                robot.rotate(self.standardRotateSpeed, 15)
            else:
                robot.move(1,0.3)

    def roundAndRoundY(self, robot, col):
        if(robot.isNotMoving() and self.delay(0.1)):
            if (colorCount(self.cameraData[self.FRONT], col) != 0 or colorCount(self.cameraData[self.FLEFT], col) != 0):
                robot.rotate(self.standardRotateSpeed, 15)
                return "found"
                #robot.move(2, 1)
            elif (colorCount(self.cameraData[self.LEFT], col) == 0):
                robot.rotate(-self.standardRotateSpeed, 15)
                return "lost"
            else:
                robot.move(1,0.3)
                return "found"

    def goAround(self, robot, col, dir):
        if (robot.isNotMoving() and self.delay(0.1, "goRound")):
            checkClose = self.FLEFT if dir == -1 else self.FRIGHT 
            checkFar = self.LEFT if dir == -1 else self.RIGHT
            if (colorCount(self.cameraData[self.FRONT], col)):
                robot.rotate(-self.standardRotateSpeed * dir, 15)
                return "front"
            elif (colorCount(self.cameraData[checkClose], col)):
                robot.rotate(-self.standardRotateSpeed * dir, 15)
                return "close"
            elif (colorCount(self.cameraData[checkFar], col)):
                robot.move(self.standardSpeed, 1)
                return "move"
            if (anyColorOf(self.cameraData, col)):
                robot.rotate(-self.standardRotateSpeed * dir, 15)
            else:
                robot.rotate(self.standardRotateSpeed * dir, 15)
            return "lost"

algo = ReallyDumb()

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    algo.run(robot, time)

run.cameraSplits = 5
run.algo = algorithm
run.isSim = False
run.debugCamera = False
run.scenario = "Internet"
run.startingOffsetError = (2,2)


run.run()



