from robot import Robot
import time

def no_algorithm():
    pass

roberto = Robot(no_algorithm)
accel_vals = []
speed_changes = []
speed = 15
accel = 0

for i in range(-10,10):
    accel = 0
    count = 0
    if i < 0:
        roberto.left.setSpeed(speed + i)
        roberto.right.setSpeed(speed)
    elif i > 0:
        roberto.right.setSpeed(speed - i)
        roberto.left.setSpeed(speed)
    t = time.time()
    while(time.time() - t < 5):
        roberto.serial.receiveData()
        accel += roberto.serial.getAccelY()
        count += 1
    print(f'speed: {i} accel y: {accel / count}')
