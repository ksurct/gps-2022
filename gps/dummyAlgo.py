import run
import random
import pygame

mod = 0
# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            robot.rotate(-90, 45)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            robot.move(100, 200)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            robot.move(-100, 200)
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            robot.rotate(90, 45)
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            robot.stop()

    # 'events' from pygame
    # 'time' time since start of program in seconds
    sensorData = robot.getSensorData()
    cameraData = robot.getCameraData()

    # in degrees
    angle = robot.getAngle()
    # Probable x,y coordinates
    position = robot.getPosition()
    print("------------------")
    for sensorName in sensorData:
        print(sensorName, 'distance =', sensorData[sensorName])

    for cameraName in cameraData.keys():
        camera = cameraData[cameraName]
        # Do something
        for split in camera:
            print("[", end="")
            for object in split:
                print(object, end="")
            print("]")

    if (sensorData['Front'] < 100 and sensorData['Front'] != -1):
        while (mod == 0):
            mod = random.randrange(-1,2)
        robot.rotate(2 * mod, 35)
    elif (robot.isNotMoving()):
        mod = 0
        robot.constantMove(2)

run.algo = algorithm

run.run()
