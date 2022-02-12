import pyglet

from robot import Robot

r = Robot()
initialMoveSpeed = 1
initialRotateSpeed = 15

window = pyglet.window.Window(width=50, height=50)


@window.event
def on_key_press(key, mod):
    global r
    global initialMoveSpeed
    global initialRotateSpeed
    key = chr(key)
    print("Pressed", key)

    if key == "w":
        # Forward
        r.constantMove(initialMoveSpeed)

    elif key == "s":
        # Backward
        r.constantMove(-initialMoveSpeed)

    elif key == "d":
        # Rotate right
        r.constantRotate(initialRotateSpeed)

    elif key == "a":
        # Rotate left
        r.constantRotate(-initialRotateSpeed)

    elif key == "=":  # = means +
        # Increase move speed
        initialMoveSpeed += 1
        r.constantMove(initialMoveSpeed)
        print("Movement Speed increased to " + str(initialMoveSpeed))

    elif key == "-":
        # Decrease move speed
        if initialMoveSpeed != 0:
            initialMoveSpeed -= 1
        r.constantMove(initialMoveSpeed)
        print("Movement Speed decreased to " + str(initialMoveSpeed))

    elif key == "]":
        # Increase rotation speed
        initialRotateSpeed += 15
        r.constantRotate(initialRotateSpeed)
        print("Rotate Speed increased to " + str(initialRotateSpeed))

    elif key == "[":
        # Decrease rotation speed
        if initialRotateSpeed != 0:
            initialRotateSpeed -= 15
        r.constantRotate(initialRotateSpeed)
        print("Rotate Speed decreased to " + str(initialRotateSpeed))

    elif key == "q" or initialMoveSpeed == 0:
        # Stop
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