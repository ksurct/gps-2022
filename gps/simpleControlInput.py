import pyglet

from robot import Robot

r = Robot()
initialSpeed = 1

window = pyglet.window.Window(width=50, height=50)


@window.event
def on_key_press(key, mod, moveSpeed, rotateSpeed):
    key = chr(key)
    print("Pressed", key)

    if key == "w":
        # Forward
        r.constantMove(moveSpeed)
    elif key == "s":
        # Backward
        r.constantMove(-moveSpeed)
    elif key == "d":
        # Rotate right
        r.constantRotate(rotateSpeed)
    elif key == "a":
        # Rotate left
        r.constantRotate(-rotateSpeed)
    elif key == "=":  # = means +
        # Increase speed
        moveSpeed += 1
    elif key == "-":
        # Decrease speed
        moveSpeed -= 1
    elif key == "q" or moveSpeed == 0:
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
