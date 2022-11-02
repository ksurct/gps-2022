from multiprocessing.connection import wait
import pyglet

from robot import Robot
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
led = 16
GPIO.setup(led, GPIO.OUT)

def a(t):
    return

r = Robot(a)
initialMoveSpeed = .2
initialRotateSpeed = 1
stopped = True

window = pyglet.window.Window(width=50, height=50)


@window.event
def on_key_press(key, mod):
    global led
    global r
    global initialMoveSpeed
    global initialRotateSpeed
    global stopped
    GPIO.output(led, GPIO.HIGH)
    key = chr(key)
    print("Pressed", key)

    if key == "w":
        # Forward
        r.constantMove(initialMoveSpeed * 4)
        stopped = False

    elif key == "s":
        # Backward
        r.constantMove(-initialMoveSpeed * 4)
        stopped = False

    elif key == "d":
        # Rotate right
        r.constantRotateNoSim(initialRotateSpeed)
        stopped = False

    elif key == "a":
        # Rotate left
        r.constantRotateNoSim(-initialRotateSpeed)
        stopped = False

    elif key == "=":  # = means +
        # Increase move speed
        initialMoveSpeed += .2
        if not stopped:
            r.constantMove(initialMoveSpeed * 4)
        print("Movement Speed increased to " + str(initialMoveSpeed * 4))

    elif key == "-":
        # Decrease move speed
        print("Movement Speed" + str(initialMoveSpeed * 4))
        initialMoveSpeed -= 1
        if (initialMoveSpeed <= 0):
            initialMoveSpeed = 0
            print("Movement Speed modified " + str(initialMoveSpeed * 4))
            stopped = True
            r.stop()
        if not stopped:
            r.constantMove(initialMoveSpeed * 4)
        print("Movement Speed decreased to " + str(initialMoveSpeed * 4))

    elif key == "]":
        # Increase rotation speed
        initialRotateSpeed *= 1.1
        if not stopped:
            r.constantRotateNoSim(initialRotateSpeed)
        print("Rotate Speed increased to " + str(initialRotateSpeed))

    elif key == "[":
        # Decrease rotation speed
        initialRotateSpeed /= 1.1
        if not stopped:
            r.constantRotateNoSim(-initialRotateSpeed)
        print("Rotate Speed decreased to " + str(initialRotateSpeed))

    elif key == "q" or initialMoveSpeed == 0:
        # Stop
        GPIO.output(led, GPIO.LOW)
        stopped = True
        r.stop()
    elif key == "o":
        #donut (360)
        r.constantRotateNoSim(2)
        wait(5)
        stopped = False
    elif key == "b":
        #boost
        r.constantMove(initialMoveSpeed+0.3)
        stopped = False
    elif key == "8":
        #figure 8
        r.constantRotateNoSim(2)
        wait(2.5)
        r.constantRotateNoSim(-2)
        wait(5)
        r.constantRotateNoSim(2)
        wait(2.5)
        stopped = False

    else:
        r.constantRotateNoSim(0)
        r.constantMove(0)
        stopped = True
    




@window.event
def on_key_release(key, mod):
    global led
    global r
    global initialMoveSpeed
    global initialRotateSpeed
    global stopped
    GPIO.output(led, GPIO.HIGH)
    key = chr(key)
    print("Pressed", key)

    if key == "w":
        # Forward
        r.constantMove(initialMoveSpeed * 4)
        stopped = False

    elif key == "s":
        # Backward
        r.constantMove(-initialMoveSpeed * 4)
        stopped = False

    elif key == "d":
        # Rotate right
        r.constantRotateNoSim(initialRotateSpeed)
        stopped = False

    elif key == "a":
        # Rotate left
        r.constantRotateNoSim(-initialRotateSpeed)
        stopped = False

    elif key == "=":  # = means +
        # Increase move speed
        initialMoveSpeed += .2
        if not stopped:
            r.constantMove(initialMoveSpeed * 4)
        print("Movement Speed increased to " + str(initialMoveSpeed * 4))

    elif key == "-":
        # Decrease move speed
        print("Movement Speed" + str(initialMoveSpeed * 4))
        initialMoveSpeed -= 1
        if (initialMoveSpeed <= 0):
            initialMoveSpeed = 0
            print("Movement Speed modified " + str(initialMoveSpeed * 4))
            stopped = True
            r.stop()
        if not stopped:
            r.constantMove(initialMoveSpeed * 4)
        print("Movement Speed decreased to " + str(initialMoveSpeed * 4))

    elif key == "]":
        # Increase rotation speed
        initialRotateSpeed *= 1.1
        if not stopped:
            r.constantRotateNoSim(initialRotateSpeed)
        print("Rotate Speed increased to " + str(initialRotateSpeed))

    elif key == "[":
        # Decrease rotation speed
        initialRotateSpeed /= 1.1
        if not stopped:
            r.constantRotateNoSim(-initialRotateSpeed)
        print("Rotate Speed decreased to " + str(initialRotateSpeed))

    elif key == "q" or initialMoveSpeed == 0:
        # Stop
        GPIO.output(led, GPIO.LOW)
        stopped = True
        r.stop()



def rel(key):
    print("Something released")


# listener = keyboard.Listener(onpress=on_press, onrelease=rel)
# with keyboard.Listener(onpress=on_press, onrelease=rel) as l:
#    l.join()
pyglet.app.run()

import time

while (True):
    print("Done")
    time.sleep(1)