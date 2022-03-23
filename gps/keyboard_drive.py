import pyglet
from motor import Motor

from robot import Robot

r = Robot()

window = pyglet.window.Window(width=10, height=10)
@window.event
def on_key_press(key, mod):
    key = chr(key)
    print("Pressed", key)

    if (key == "w"):
        # Forward
        pass
    elif (key == "s"):
        # Backward
        pass
    elif (key == "d"):
        # Rotate right
        pass
    elif (key == "a"):
        # Rotate left
        pass
    elif (key == "q"):
        # Stop
        pass

def rel(key):
    print("Something released")
    
#listener = keyboard.Listener(onpress=on_press, onrelease=rel)
#with keyboard.Listener(onpress=on_press, onrelease=rel) as l:
#    l.join()
pyglet.app.run()

import time
while (True):
    print("Done")
    time.sleep(1)