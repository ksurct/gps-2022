
def run(robot, time):
    isBluePresent = False
    for obj in robot.getCameraData():
        print(obj)
        if obj.getColor() == 'Blue':
            isBluePresent = True
    if isBluePresent:
        robot.stop()
    else:
        robot.move(.5, 1)