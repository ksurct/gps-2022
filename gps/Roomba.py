
def run(robot, time):
    distances = robot.getSensorData()
    minDistance = distances['Right']
    minDistanceSensorName = 'Right'

    # find min distance and its associated sensor
    for sensorName in distances.keys():
        print(minDistance)
        distance = distances[sensorName]
        if distance < minDistance and distance > 0:
            minDistance = distance
            minDistanceSensorName = sensorName

    rotateDistance = 9.0
    rotateTime = 1
    rotateSpeed = rotateDistance / rotateTime
    moveDistance = .1
    moveTime = .1
    moveSpeed = moveDistance/moveTime

    action = None

    # turn away from min distance
    # Right side is closest
    if minDistanceSensorName == 'Right' or minDistanceSensorName == 'FrontRight':
        if minDistance < 10:
            action = 'Left'
    # Left side is closest
    if minDistanceSensorName == 'Left' or minDistanceSensorName == 'FrontLeft':
        if minDistance < 10:
            action = 'Right'
    # Front side is closest
    if minDistanceSensorName == 'Front':
        if minDistance < 10:
            action = 'Spin'
        
    if action == 'Right':
        robot.rotate(-rotateSpeed, rotateDistance)
    elif action == 'Left':
        robot.rotate(rotateSpeed, rotateDistance)
    elif action == 'Spin':
        robot.rotate(9.0 / rotateTime, 9)
    else:
        robot.move(moveSpeed, moveDistance)