import timeit
import time

def run(robot, t, events=None):
    
    distances = robot.getSensorData()
    minDistance = 10000
    minDistanceSensorName = "Nothing Close"

    # find min distance and its associated sensor
    for sensorName in distances.keys():
        # print(minDistance)
        distance = distances[sensorName]
        if distance < minDistance and distance > 0:
            minDistance = distance
            minDistanceSensorName = sensorName

    rotateDistance = 2000
    rotateTime = 1
    rotateSpeed = rotateDistance / rotateTime
    moveDistance = 2500
    moveTime = 1
    moveSpeed = moveDistance / moveTime

    action = 'Forward'

    # turn away from min distance
    # Right side is closest
    if minDistanceSensorName == "Nothing Close":
        action = 'Forward'
    elif minDistanceSensorName == 'Right' or minDistanceSensorName == 'FrontRight':
        if minDistance < 60:
            print(minDistance)
            action = 'Left'
    # Left side is closest
    elif minDistanceSensorName == 'Left' or minDistanceSensorName == 'FrontLeft':
        if minDistance < 60:
            action = 'Right'
    # Front side is closest
    elif minDistanceSensorName == 'Front':
        if minDistance < 60:
            action = 'Spin'

    if action == 'Forward':
        robot.move(moveSpeed, moveDistance)
        print(minDistance)
        #robot.ledOn('yellow', True)
        print(action)    
    elif action == 'Right':
        robot.rotate(rotateSpeed, rotateDistance)
        #robot.ledOn('yellow', True)
        print(action)
    elif action == 'Left':
        robot.rotate(-rotateSpeed, rotateDistance)
        #robot.ledOn('yellow', True)
        print(action)
    elif action == 'Spin':
        robot.rotate(-rotateSpeed, rotateDistance)
        #robot.ledOn('red', True)
        print(action)
    else:
        robot.move(moveSpeed, moveDistance)
        #robot.ledOn('green', True)
        print('Forward')
        print(minDistance)