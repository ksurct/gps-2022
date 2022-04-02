import run
import random
import pygame

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
        if (sensorData["Front"] < 0.25):
            robot.stop()
            self.overrodeAction = True

    def init(self, robot, time):
        print(robot.getPosition())
        return "INIT"

    def corner1(self, robot, time):
        robot.constantMove(self.standardSpeed)
        return "CORNER1"

    def corner2(self, robot, time):
        return "CORNER2"

    def corner3(self, robot, time):
        return "CORNER3"

    def corner4(self, robot, time):
        return "CORNER4"

    def red(self, robot, time):
        return "RED"

    def yellow(self, robot, time):
        return "YELLOW"

    def run(self, robot, time):
        self.state = self.states[self.state](robot, time)


algo = ReallyDumb()

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    algo.run(robot, time)

run.algo = algorithm
run.isSim = True
run.run()

