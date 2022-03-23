import pyglet

from robot import Robot
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
led = 16
GPIO.setup(led, GPIO.OUT)

r = Robot()
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
        r.constantMove(initialMoveSpeed)
        stopped = False

    elif key == "s":
        # Backward
        r.constantMove(-initialMoveSpeed)
        stopped = False

    elif key == "d":
        # Rotate right
        r.constantRotate(initialRotateSpeed)
        stopped = False

    elif key == "a":
        # Rotate left
        r.constantRotate(-initialRotateSpeed)
        stopped = False

    elif key == "=":  # = means +
        # Increase move speed
        initialMoveSpeed += .2
        if not stopped:
            r.constantMove(initialMoveSpeed)
        print("Movement Speed increased to " + str(initialMoveSpeed))

    elif key == "-":
        # Decrease move speed
        print("Movement Speed" + str(initialMoveSpeed))
        initialMoveSpeed -= 1
        if (initialMoveSpeed <= 0):
            initialMoveSpeed = 0
            print("Movement Speed modified " + str(initialMoveSpeed))
            stopped = True
            r.stop()
        if not stopped:
            r.constantMove(initialMoveSpeed)
        print("Movement Speed decreased to " + str(initialMoveSpeed))

    elif key == "]":
        # Increase rotation speed
        initialRotateSpeed += 1
        if not stopped:
            r.constantRotate(initialRotateSpeed)
        print("Rotate Speed increased to " + str(initialRotateSpeed))

    elif key == "[":
        # Decrease rotation speed
        initialRotateSpeed -= 5
        if (initialRotateSpeed <= 0):
            initialRotateSpeed = 0
            stopped = True
        if not stopped:
            r.constantRotate(-initialRotateSpeed)
        print("Rotate Speed decreased to " + str(initialRotateSpeed))

    elif key == "q" or initialMoveSpeed == 0:
        # Stop
        GPIO.output(led, GPIO.LOW)
        stopped = True
        r.stop()


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
        r.constantMove(initialMoveSpeed)
        stopped = False

    elif key == "s":
        # Backward
        r.constantMove(-initialMoveSpeed)
        stopped = False

    elif key == "d":
        # Rotate right
        r.constantRotate(initialRotateSpeed)
        stopped = False

    elif key == "a":
        # Rotate left
        r.constantRotate(-initialRotateSpeed)
        stopped = False

    elif key == "=":  # = means +
        # Increase move speed
        initialMoveSpeed += .2
        if not stopped:
            r.constantMove(initialMoveSpeed)
        print("Movement Speed increased to " + str(initialMoveSpeed))

    elif key == "-":
        # Decrease move speed
        print("Movement Speed" + str(initialMoveSpeed))
        initialMoveSpeed -= 1
        if (initialMoveSpeed <= 0):
            initialMoveSpeed = 0
            print("Movement Speed modified " + str(initialMoveSpeed))
            stopped = True
            r.stop()
        if not stopped:
            r.constantMove(initialMoveSpeed)
        print("Movement Speed decreased to " + str(initialMoveSpeed))

    elif key == "]":
        # Increase rotation speed
        initialRotateSpeed += 1
        if not stopped:
            r.constantRotate(initialRotateSpeed)
        print("Rotate Speed increased to " + str(initialRotateSpeed))

    elif key == "[":
        # Decrease rotation speed
        initialRotateSpeed -= 5
        if (initialRotateSpeed <= 0):
            initialRotateSpeed = 0
            stopped = True
        if not stopped:
            r.constantRotate(-initialRotateSpeed)
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