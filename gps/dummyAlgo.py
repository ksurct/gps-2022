from multiprocessing.connection import wait
import run
import time

mod = 0
state = "MOVE"


def colorCount(split, color):
    for obj in split:
        if (obj["color"] == color):
            return True
    return False

class ReallyDumb():
    def __init__(self) -> None:
        self.state = "INIT"
        self.standardSpeed = 5
        self.standardRotateSpeed = 720
        self.overrodeAction = False
        self.waitCall = None
        self.waitCallTime = None
        self.time = 0
        self.states = {
            "INIT": self.init,
            "CORNER1": self.corner1,
            "YELLOW": self.yellow,
            "CORNER2": self.corner2,
            "CORNER3": self.corner3,
            "RED": self.red,
            "CORNER4": self.corner4
        }
    
    def overrideCheck(self, robot, time):
        sensorData = robot.getSensorData()
        if (sensorData["Front"] < 0.25 and sensorData["Front"] != -1):
            robot.stop()
            self.overrodeAction = True

    def init(self, robot, time):
        self.wait(lambda r, t: r.rotate(720, 15), 1)
        return "CORNER1"

    def corner1(self, robot, time):
        self.wait(lambda r, t: r.rotate(-720, 15), 1)
        return "CORNER2"

    def corner2(self, robot, time):
        self.wait(lambda r, t: r.move(1, 1.5), 1)
        return "CORNER3"

    def corner3(self, robot, time):
        self.wait(lambda r, t: r.move(-1, 1.5), 1)
        return "CORNER4"

    def corner4(self, robot, time):
        self.wait(lambda r, t: r.move(1, 1.5), 1)
        return "RED"

    def red(self, robot, time):
        self.wait(lambda r, t: r.rotate(720, 180), 1)
        return "YELLOW"

    def yellow(self, robot, time):
        self.wait(lambda r, t: r.rotate(-720, 180), 1)
        return "CORNER1"

    def wait(self, waitCall, delay):
        self.waitCall = waitCall
        self.waitCallTime = self.time + delay

    def runWait(self, robot, time):
        self.waitCall(robot, time)
        self.waitCall = None

    def run(self, robot, time):
        self.time = time
        self.overrideCheck(robot, time)
        if (self.waitCall != None):
            if (self.waitCallTime < time):
                self.runWait(robot, time)
            else:
                return
        ret = self.states[self.state](robot, time)
        if ret != None:
            self.state = ret


algo = ReallyDumb()

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    algo.run(robot, time)

run.algo = algorithm
run.isSim = True
run.run()

