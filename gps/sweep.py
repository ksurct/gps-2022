from robot import Robot
import time

def no_algorithm():
    pass

roberto = Robot(no_algorithm)
accel_vals = []
speed_changes = []
speed = 5
accel = 0

for i in range(-5,5):
    accel = 0
    count = 0
    if i < 0:
        roberto.left.setSpeed(-50)
        roberto.right.setSpeed(50)
    elif i > 0:
        roberto.right.setSpeed(-50)
        roberto.left.setSpeed(50)
    t = time.time()
    while(time.time() - t < 5):
        roberto.serial.receiveData()
        accel += roberto.serial.getAccelY()
        count += 1
    print(f'speed: {i} accel y: {accel / count}')
