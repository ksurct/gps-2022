
from numpy import diff
import run

mod = 0
state = "MOVE"
#sensor check
def sCheck(value, distance):
    return value < distance and value != -1

class Margin():
    def __init__(self, a, b, standard=True):
        self.a = a
        self.b = b
        self.standard = standard
    
    def contains(self, angle):
        if (self.standard):
            return angle > self.a and angle < self.b
        return angle < self.a or angle > self.b

    def optimal(self):
        if (self.standard):
            return (self.a + self.b) / 2
        diff = 360 - self.b + self.a
        return (diff/2 + self.b) % 360

    def turnValue(self, angle):
        opt = self.optimal()

        diff = (opt - angle) % 360
        diff2 = (angle - opt) % 360
        print(opt)
        print(diff)
        print(diff2)
        if (abs(diff2) < abs(diff)):
            diff = diff2
        if (diff > 180):
            return 360 - diff
        return -diff

def anyColorOf(data, col):
    for split in data:
        for obj in split:
            if (obj["color"] == col):
                return True
    return False

def colorCount(split, color):
    count = 0
    for obj in split:
        if (obj["color"] == color):
            count += 1
    return count

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
        self.standardRotateSpeed = 900
        def dsen():
            return {"Front": -1, "FrontRight": -1, "FrontLeft": -1, "Left": -1, "Right": -1}
        self.sensorList = [dsen(), dsen(), dsen()]
        self.overrodeAction = False
        self.waitQueue = []
        self.currentWait = None
        self.vars = {}
        self.var = None
        self.time = 0
        self.cameraData = [[],[],[],[],[]]
        self.LEFT = 0
        self.callSensorListOnce = True
        self.FLEFT = 1
        self.FRONT = 2
        self.sensorValid = 5
        self.FRIGHT = 3
        self.RIGHT = 4
        self.delays = {}
        self.sensorData = None
        self.objCount = 1
        self.sdt = 1

        self.periodic = {}
        self.states = {
            "INIT": self.init,
            "FIND_CORNER1": self.findState("CORNER1", "Blue"),
            "FIND_CORNER2": self.findState("CORNER2", "Yellow"),
            "FIND_CORNER3": self.findState("CORNER3", "Blue"),
            "FIND_CORNER4": self.findState("CORNER4", "Blue"),
            "FIND_CORNER5": self.findState("CORNER5", "Blue"),
            "CORNER1": self.turnState("CORNER2_STITCH", "Blue", 1, Margin(135, 160)),
            "CORNER2": self.turnState("CORNER3_STITCH", "Yellow", -1, Margin(40, 60)),
            "CORNER3": self.turnState("CORNER4_STITCH", "Blue", 1, Margin(-180 + 360, -160 + 360)),
            "CORNER4": self.turnState("RED_STITCH", "Blue", 1, Margin(-100 + 360, -80 + 360)),
            "CORNER5": self.turnState("CORNER1_STITCH", "Blue", 1, Margin(10, -10 + 360, False)),
            "RED_STITCH": self.stitchState("FIND_RED", "Red", Margin(-100 + 360,-90 + 360)),
            "CORNER1_STITCH": self.stitchState("FIND_CORNER1", "Blue", Margin(10, -10 + 360, False)),
            "CORNER2_STITCH": self.stitchState("FIND_CORNER2", "Yellow", Margin(100,120)),
            "CORNER3_STITCH": self.stitchState("FIND_CORNER3", "Blue", Margin(35,50)),
            "CORNER4_STITCH": self.stitchState("FIND_CORNER4", "Blue", Margin(165, -165 + 360)),
            "CORNER5_STITCH": self.stitchState("FIND_CORNER5", "Blue", Margin(-100 + 360,-80 + 360)),
            "SPIN": self.spin,
            "FIND_RED": self.findRed,
            "LEFT_RED": self.redTurnState("CORNER5_STITCH", -1),
            "RIGHT_RED": self.redTurnState("CORNER5_STITCH", 1)
        }

    def updateSensors(self, robot, time):
        print("called")
        self.sensorData = robot.getSensorData()

    def getSensorList(self, robot):
        if (self.callSensorListOnce):
            data = robot.getSensorData()
            self.sensorList.insert(0, data)
            self.sensorList.pop(len(self.sensorList) - 1)
            self.callSensorListOnce = False
        return self.sensorList

    def updateCamera(self, robot, time):
        self.cameraData = bigestColors(robot.getCameraData()["main"], self.objCount)

    def findState(self, nextState, color):
        def fun(robot, time):
            if (self.findColor(robot, time, color)):
                ret = self.ramColor(robot, time, color)
                if (ret == "Done"):
                    return nextState
        return fun

    def turnState(self, nextState, color, dir, angleMargin):
        def fun(robot, time):
            if (self.var == None):
                self.var = 0
            ret = self.goAroundWithSensors(robot, color, dir)
            angle = robot.getAngle()
            if (angle < 0):
                angle += 360
            if (angleMargin.contains(angle)):
                return nextState
            # if (ret == "move"):
            #     self.var += 1
            # if (self.var > 3 ):
            #     self.var = None
            #     return nextState
        return fun

    def stitchState(self, nexState, color, angleMargin):
        def fun(robot, time):
            if (robot.isNotMoving()):
                robot.move(self.standardSpeed*2, 1)
            elif (colorCount(self.cameraData[self.FRONT], color) != 0
                    or colorCount(self.cameraData[self.FLEFT], color) != 0
                    or colorCount(self.cameraData[self.FRIGHT], color) != 0
                    or colorCount(self.cameraData[self.RIGHT], color) != 0
                    or colorCount(self.cameraData[self.LEFT], color) != 0):
                return nexState
        return fun

    def spin(self, robot, time):
        robot.constantRotate(self.standardRotateSpeed)

    def printUpdate(self, robot, time):
        pass
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
        # print("State: " + self.state)


    def overrideCheck(self, robot, time):
        pass
        # sensorData = robot.getSensorData()
        # if (sensorData["Front"] < 0.2 and sensorData["Front"] != -1):
        #     robot.stop()
        #     self.overrodeAction = True

    def redTurnState(self, nextState, dir):
        def fun(robot, time):

            if (self.var == None):
                self.var = 0
            if (self.var > 0):
                angle = robot.getAngle()
                if (robot.isNotMoving()):
                    robot.rotate(dir*self.standardRotateSpeed, 20)
                if (angle > -100 and angle < -80):
                    self.var = None
                    return nextState
            elif (self.goAround(robot, "Red", dir) == "move"):
                self.var += 1
        return fun

    def findRed(self, robot, time):
        self.objCount = 2
        data = self.getSensorList(robot)[0]
        ret = None
        if (sCheck(data["Front"], 0.5)):
            val = self.var
            robot.stop()
            self.var = None
            if (val == "FLEFT" or val == "LEFT"):
                return "RIGHT_RED"
            if (val == "FRIGHT" or val == "RIGHT"):
                return "LEFT_RED"
        if (colorCount(self.cameraData[self.LEFT], "Red")):
            self.var = "LEFT"
        elif (colorCount(self.cameraData[self.RIGHT], "Red")):
            self.var = "RIGHT"
        elif (colorCount(self.cameraData[self.FRIGHT], "Red")):
            self.var = "FRIGHT" if self.var != "RIGHT" or self.var != "LEFT" else self.var
        elif (colorCount(self.cameraData[self.FLEFT], "Red")):
            self.var = "FLEFT" if self.var != "RIGHT" or self.var != "LEFT" else self.var
        if (self.findColor(robot, time, "Red")):
            robot.move(self.standardSpeed,1)

    def init(self, robot, time):
        self.addPeriodic("camera", self.updateCamera, 0.1)                          
        self.addPeriodic("status", self.printUpdate, 0.2)
        # self.addPeriodic("sensors", self.updateSensors, 0.1)
        robot.initAngle()
        if (self.delay(1, "Something")):
            return "CORNER1_STITCH"

    def ramColor(self, robot, time, color):
        sensorData = self.getSensorList(robot)[0]
        if (colorCount(self.cameraData[self.FRONT], color) == 0):
            return "Lost"
        if (sCheck(sensorData["Front"], 0.7)):
            # or sCheck(sensorData["FrontLeft"], 0.4)
            # or sCheck(sensorData["FrontRight"], 0.4)):
            robot.stop()
            return "Done"
        else:
            robot.constantMove(self.standardSpeed*.8)
            return "Move"


    def findColor(self, robot, time, col):
        delayTime = 0.8
        sensorData = self.getSensorList(robot)
        if (sCheck(sensorData[0]["Front"], 0.7)):
            return True

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

    def ramObject(self, robot, time):
        sensorData = self.getSensorList(robot)[0]
        if (sCheck(sensorData["Front"], 0.7)):
            robot.stop()
            return "Done"
        elif (sCheck(sensorData["Front"], self.sensorValid)):
            robot.constantMove(self.standardSpeed*0.7)
        else:
            return "Lost"

    def findObject(self, robot, time):
        if (robot.isNotMoving() and self.delay(0.5)):
            print("Running")
            sensorData = self.getSensorList(robot)
            if (sCheck(sensorData[0]["Front"], self.sensorValid)):
                print("Found")
                return True

            for i in range(len(sensorData)):
                print(i)
                s = sensorData[i]
                # Previous front detection
                if sCheck(s["Front"], self.sensorValid):
                    print("Cluel4")
                    robot.rotate(self.standardRotateSpeed, 20); break
                elif sCheck(s["FrontLeft"], self.sensorValid):
                    print("Cluel3")
                    robot.rotate(-self.standardRotateSpeed, 20); break
                elif sCheck(s["FrontRight"], self.sensorValid):
                    print("Cluel2")
                    robot.rotate(self.standardRotateSpeed, 20); break
                elif sCheck(s["Left"], self.sensorValid):
                    print("Cluel1")
                    robot.rotate(-self.standardRotateSpeed, 40); break
                elif sCheck(s["Right"], self.sensorValid):
                    print("Cluelesss")
                    robot.rotate(self.standardRotateSpeed, 40); break
                else: # No idea
                    print("Clueless")
                    robot.rotate(self.standardRotateSpeed, 15); break
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
        self.callSensorListOnce = True
        self.runPeriodic(robot, time)
        self.overrideCheck(robot, time)
        if (self.runWait(robot, time)):
            return
        ret = self.states[self.state](robot, time)
        if ret != None and ret != self.state:
            print("Changing to state:", ret)
            self.state = ret

    def goAround(self, robot, col, dir):
        if (robot.isNotMoving() and self.delay(0.1, "goRound")):
            checkClose = self.FLEFT if dir == -1 else self.FRIGHT 
            checkFar = self.LEFT if dir == -1 else self.RIGHT
            if (colorCount(self.cameraData[self.FRONT], col)):
                robot.rotate(-self.standardRotateSpeed * dir, 20)
                return "front"
            elif (colorCount(self.cameraData[checkClose], col)):
                robot.rotate(-self.standardRotateSpeed * dir, 20)
                return "close"
            elif (colorCount(self.cameraData[checkFar], col)):
                robot.move(self.standardSpeed, 1)
                return "move"
            if (anyColorOf(self.cameraData, col)):
                robot.rotate(-self.standardRotateSpeed * dir, 20)
                return "far"
            else:
                robot.rotate(self.standardRotateSpeed * dir, 20)
            return "lost"

    def goAroundWithSensors(self, robot, col, dir):
        if (robot.isNotMoving() and self.delay(0.1, "goRound")):
            data = self.getSensorList(robot) # {[],[],[],[],[]}
            closeIndex = "FrontLeft" if dir == -1 else "FrontRight"
            farIndex = "Left" if dir == -1 else "Right"
            frontIndex = "Front"
            checkClose = data[0][closeIndex]
            checkFar = data[0][farIndex]
            checkFront = data[0][frontIndex]

            if sCheck(checkFront, 1.5):
                robot.rotate(-self.standardRotateSpeed * dir, 2*30)
                return "front"
            elif sCheck(checkClose, 1.5):
                robot.rotate(-self.standardRotateSpeed * dir, 30)
                return "close"
            elif sCheck(checkFar, 1.5):
                robot.move(self.standardSpeed, .5)
                print("move forward")
                return "move"
            else:
                for i in range(len(data)):
                    s= data[i]
                    if sCheck(s[frontIndex], 1.5):
                        robot.rotate(-self.standardRotateSpeed * dir, 2*30)
                        return "front"
                    elif sCheck(s[closeIndex], 1.5):
                        robot.rotate(-self.standardRotateSpeed * dir, 30)
                        return "close"
                    elif sCheck(s[farIndex], 1.5) and i == 1:
                        robot.rotate(self.standardRotateSpeed * dir, 30)
                        return "far"
                robot.rotate(self.standardRotateSpeed * dir, 30)
                return "lost"

if (__name__ == "__main__"):
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
    run.scenario = "MAIN"
    run.startingOffsetError = (2,2)


    run.run()

    m = Margin(170, -170 + 360, False)

    print("Test = ", m.optimal())

    print("Test = ", m.contains(-176))

    print("Test = ", m.turnValue(90))
