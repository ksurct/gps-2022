
def run(robot, time):
    if (int(time) % 2 == 1):
        robot.rotate(9, 9)
        print(time)
        print('right')
    else:
        robot.rotate(-9, 9)
        print(time)
        print('left')