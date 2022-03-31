import run
import random
import pygame

mod = 0
state = "MOVE"


# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    global state
    if (robot.isNotMoving()):

        if (state == "MOVE"):
            print("Move")
            robot.move(1, 2)
            state = "ROTATE"
        elif (state == "ROTATE"):
            print("Running")
            robot.rotate(90, 180)
            state = "MOVE"
run.algo = algorithm

run.run()
