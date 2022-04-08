

from buttons import Button

import run

from dummyAlgo import ReallyDumb


def normal(pin):
    algo = ReallyDumb()
    run.cameraSplits = 5
    run.algo = algorithm
    run.isSim = False
    run.debugCamera = "Internet"
    run.scenario = "MAIN"
    run.startingOffsetError = (2,2)
    def algorithm(robot, time, events = None):
        algo.run(robot, time)

    run.run()

def fast(pin):
    print("fast")

def terminal(pin):
    print("terminal")

def escapeVelocity(pin):
    print("escapeVelocity", pin)

b1 = Button(11, normal) 
b2 = Button(25, fast) 
b3 = Button(8, terminal) 
b4 = Button(7, escapeVelocity)

