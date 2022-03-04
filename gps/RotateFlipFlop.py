
def run(robot, time):
    if (int) time % 2 == 1:
        robot.rotate(90, 90)
    else:
        robot.rotate(90, -90)