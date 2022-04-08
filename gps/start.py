

from buttons import Button

import run

from dummyAlgo import ReallyDumb


def normal(pin):
    algo = ReallyDumb()

    def algorithm(robot, time, events = None):
        algo.run(robot, time)

    run.cameraSplits = 5
    run.algo = algorithm
    run.isSim = False
    run.debugCamera = False
    run.scenario = "MAIN"
    run.startingOffsetError = (2,2)

    run.run()

def fast(pin):
    normal(pin)

def terminal(pin):
    normal(pin)

def escapeVelocity(pin):
    normal(pin)

b1 = Button(11, normal) 
b2 = Button(25, fast) 
b3 = Button(8, terminal) 
b4 = Button(7, escapeVelocity)

