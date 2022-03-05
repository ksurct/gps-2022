import time
import buttons

def callibrateDistance(robot, time):
    
    #if not robot.isMoving():
    #    robot.move(.25, 1)
    
    functions = [moveMeters, moveMeters, moveMeters, moveMeters]
    if (not robot.buttonsPopulated):
        robot.buttonsSetup(functions)
    
 # constant time || button # at pin corrisponds to meters (i.e. button 2 goes 2 meters)
def moveMeters(robot, pin):
    duration = 1 # in seconds
    distance = 1
    found = False
    for i in range(4):
        if pin == robot.buttonPins[i]:
            distance = i + 1
            found = True
    print('Moving %s meters', distance)
    print(found)
    robot.move(distance / duration, distance)