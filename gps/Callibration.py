import time
from buttons import Button

robot = None
button1 = False
button2 = False
button3 = False
button4 = False
buttonPins = [11, 25, 8, 7]
tim = time.time()

 # constant time || button # at pin corrisponds to meters (i.e. button 2 goes 2 meters)
def moveOneMeters(pin):
    global button1
    button1 = True

def rotate90DegreesLeft(pin):
    global button3
    button3 = True

def rotate90DegreesRight(pin):
    global button4
    button4 = True

def callibrateDistance(r, t):
    robot = r
    global button1
    global button2
    global button3
    global button4
    if button1:
        robot.move(1, 1)
        button1 = False
    if button3:
        print('rotate left')
        robot.rotate(90, 90)
        button3 = False
    if button4:
        print('rotate right')
        robot.rotate(-90, 90)
        button4 = False
        
Button(buttonPins[0], moveOneMeters)
Button(buttonPins[2], rotate90DegreesLeft)
Button(buttonPins[3], rotate90DegreesRight)
