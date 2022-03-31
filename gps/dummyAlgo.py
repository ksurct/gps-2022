import run
import random
import pygame

mod = 0
state = "MOVE"

def isColorIn(split, color):
    for obj in split:
        if (obj["color"] == color):
            return True
    return False

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    global state
    data = robot.getCameraData()["main"]
    print(robot.getPosition())
    if (robot.isNotMoving()):
    #if (isColorIn(data[1], "Blue")):
        if (state == "MOVE"):
            robot.move(1,0.1)
            state = "STOP"
        elif (state == "STOP"):
            robot.rotate(720, 15)
            state = "MOVE"
run.algo = algorithm
run.isSim = False
run.run()

