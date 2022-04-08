

from buttons import Button

import run
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from dummyAlgo import ReallyDumb

go = False

def normal(pin):
    global go
    go = True

def fast(pin):
    normal(pin)

def terminal(pin):
    normal(pin)

def escapeVelocity(pin):
    normal(pin)

GPIO.setmode(GPIO.BCM)

# b1 = Button(11, normal) 
# b2 = Button(25, fast) 
# b3 = Button(8, terminal) 
# b4 = Button(7, escapeVelocity)


algo = ReallyDumb()

def algorithm(robot, time, events = None):
    algo.run(robot, time)

run.cameraSplits = 5
run.algo = algorithm
run.isSim = False
run.debugCamera = False
run.scenario = "MAIN"
run.startingOffsetError = (2,2)


count = 0

GPIO.setup(11, GPIO.IN) 

while (True):
    state = GPIO.input(11)
    if (count > 10):
        run.run()
    if (not state):
        count += 1
    else:
        count = 0
