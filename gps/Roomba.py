import timeit
import time

def run(robot, t):
    
    distances = robot.getSensorData()
    robot.getSensorData
    print(time.time()-t)
    minDistance = distances['Right']
    minDistanceSensorName = 'Right'

    # find min distance and its associated sensor
    for sensorName in distances.keys():
        # print(minDistance)
        distance = distances[sensorName]
        if distance < minDistance and distance > 0:
            minDistance = distance
            minDistanceSensorName = sensorName

    rotateDistance = 2.0
    rotateTime = .1
    rotateSpeed = rotateDistance / rotateTime
    moveDistance = .25
    moveTime = .1
    moveSpeed = moveDistance / moveTime

    action = None

    # turn away from min distance
    # Right side is closest
    if minDistanceSensorName == 'Right' or minDistanceSensorName == 'FrontRight':
        if minDistance < 60:
            action = 'Left'
    # Left side is closest
    if minDistanceSensorName == 'Left' or minDistanceSensorName == 'FrontLeft':
        if minDistance < 60:
            action = 'Right'
    # Front side is closest
    if minDistanceSensorName == 'Front':
        if minDistance < 60:
            action = 'Spin'
        
    if action == 'Right':
        robot.rotate(-rotateSpeed, rotateDistance)
        robot.ledOn('yellow', True)
        print(action)
    elif action == 'Left':
        robot.rotate(rotateSpeed, rotateDistance)
        robot.ledOn('yellow', True)
        print(action)
    elif action == 'Spin':
        robot.rotate(rotateSpeed, 4*rotateDistance)
        robot.ledOn('red', True)
        print(action)
    else:
        robot.move(moveSpeed, moveDistance)
        robot.ledOn('green', True)
        print('Forward')