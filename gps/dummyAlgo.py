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
    if (isColorIn(data[1], "Red")):
        robot.rotate(270, 270)        
run.algo = algorithm

run.run()
