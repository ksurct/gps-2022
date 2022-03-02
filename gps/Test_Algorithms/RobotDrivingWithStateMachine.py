import robot_sim
import random
import pygame

# Target FPS
FPS = 60
flip = False
white = (255,255,255,255)
blue = (0,0,255,255)
green = (0,255,0,255)
red = (255,0,0,255)
yellow = (255, 255 , 0, 255)
mod = 0
flag = 0
is_blue = False
is_yellow = False
rightRed = False
leftRed = False
greenLeft = False
greenLeft = False
sped = 150
state = "straightOn"

#state = {"leftTurn", "goStraight", "turnRight", "threadNeedle", "hop", "undefined"}


def isColorInSplit(split, color):
    for object in split:
        if (object['color'] == color):
            return True
    return False


#class State(state):
    #def fguin()
#return

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events):
    global white
    global blue
    global flip
    global green
    global yellow
    global red
    global mod
    global flag
    global is_blue
    global is_yellow
    global leftRed
    global rightRed
    global morBlue
    global sped
    global camera
    global sensorData
    global state
    global greenLeft
    global greenRight
    # 'events' from pygame
    # 'time' time since start of program in seconds
    sensorData = robot.getSensorData()
    cameraData = robot.getCameraData()
    keyboard(events)
    # in degrees
    angle = robot.getAngle()
    # Probable x,y coordinates
    position = robot.getPosition()
    print("------------------")
    #for sensorName in sensorData:
        #print(sensorName, 'distance =', sensorData[sensorName])

    camera = cameraData['main']
    camera2 = cameraData['main']
    morBlu = False
    for object in camera[0]:
        if (object['color'] == blue):
            print("blue,", end="")
        elif (object['color'] == white):
            print("white,", end="")
        elif (object['color'] == green):
            print("green,", end="")
        elif (object['color'] == red):
            print("red,", end="")
    """
            #morBlu = False
        if (object['color'] == blue):
            #morBlu = False
            is_Blue = True
            """
    """
            for split in camera2:
                if (split != camera2[0]):
                    for object in split:
                        if (object['color'] == blue):
                            morBlu = True
            if (morBlu == False):
                robot.move(30,30)
                is_blue = True
            else:
                robot.rotate(30,10)
                is_blue = False
            """
    """
        else:
            if (is_blue == True):
                morBlu = False
                for split in camera2:
                    if (split != camera2[0]):
                        for object in split:
                            if (object['color'] == blue):
                                morBlu = True
                if (morBlu == False):
                    robot.constantRotate(-30)
        """
    """
    if (isColorInSplit(camera[0], blue) == False):
        if (isColorInSplit(camera[1], blue) == False):
            if (is_blue == True):
                robot.constantRotate(-30)
            else:
                is_blue = False
    else:
        is_blue = True
    if (isColorInSplit(camera[2], yellow) == False):
        if (isColorInSplit(camera[1], yellow) == False):
            if (is_yellow == True):
                robot.constantRotate(30)
        is_yellow = False
    else:
        is_yellow = True
    robot.move(30,30)
    """
    def start():
        #do stuff
        return "STOP"

    def stop():
        return "START"


    def LT():
        global is_blue
        if (isColorInSplit(camera[0], red) == True or
        isColorInSplit(camera[1], red) == True or
        isColorInSplit(camera[2], red) == True):
            return "threadNeedle"
        if (isColorInSplit(camera[2], yellow) == True):
            return "rightTurn"
        #turn left arround blue barrels
        if (isColorInSplit(camera[0], blue) == True):
            is_blue = True
            robot.move(sped,sped)
            #if (isColorInSplit(camera[1], blue) == True):
        elif (is_blue == True and isColorInSplit(camera[1], blue) == False):
            robot.constantRotate(-sped)
        elif (isColorInSplit(camera[1], blue) == True):
            robot.constantRotate(sped)
        else:
            robot.move(sped,sped)    
        return "leftTurn"

    def TN():
        global leftRed
        global rightRed
        if (isColorInSplit(camera[0], blue) == True or
        isColorInSplit(camera[1], blue) == True or
        isColorInSplit(camera[2], blue) == True):
            return "rightTurn"
        if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
            return "straightOn"
        if (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True):     #if red in left and right
            robot.move(sped,sped)                                                                       #go straight
        #elif (isColorInSplit(camera[1], red) == True):
            #robot.move(30,30)
        elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == False and rightRed == False):  #if red in left and not in right and wasnt in right last time
            if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                robot.move(sped,sped)                                                                   #go forward
            #if ()
            robot.constantRotate(-sped)                                                               #turn left
        elif (isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == True and leftRed == False):  #if red not in left and in right and wasnt in left last time
            if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                robot.move(sped,sped)                                                                   #go forward
            robot.constantRotate(sped)                                                                #turn right
        #elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True and isColorInSplit(camera[1], red) == True):    #if all red
            #robot.move(150,150)                                                                     #go straight
        elif (isColorInSplit(camera[1], red) == True):                                              #if red mid and not left or right
            robot.move(sped,sped)                                                                     #go straight
        if (isColorInSplit(camera[1], red) == True and isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == False) :
            robot.move(sped,sped)
        if (isColorInSplit(camera[0], red) == True):
            leftRed = True
        if (isColorInSplit(camera[2], red) == True):
            rightRed = True
        return "threadNeedle"

    def RT():
        global is_yellow
        if (isColorInSplit(camera[0], blue)):
            return "leftTurn"
        if (isColorInSplit(camera[0], yellow) == True):
            is_yellow = True
            robot.move(sped,sped)
            #if (isColorInSplit(camera[1], blue) == True):

        elif (is_yellow == True and isColorInSplit(camera[1], yellow) == False):
            robot.constantRotate(sped)
        elif (isColorInSplit(camera[1], yellow) == True):
            robot.constantRotate(-sped)
        else:
            robot.move(sped,sped)
        return "rightTurn"

    def SO():
        if (isColorInSplit(camera[0], blue) == True or
        isColorInSplit(camera[1], blue) == True or
        isColorInSplit(camera[2], blue) == True):
            return "leftTurn"
        if (isColorInSplit(camera[0], red) == True or
        isColorInSplit(camera[1], red) == True or
        isColorInSplit(camera[2], red) == True):
            return "threadNeedle"
        if (isColorInSplit(camera[0], red) == False or
        isColorInSplit(camera[1], red) == False or
        isColorInSplit(camera[2], red) == False):
            return "rightTurn"
        robot.move(sped,sped)
        return "straightOn"

    #def HOP():
        #global greenLeft
        #global greenRight
        #if (isColorInSplit(camera[0], blue)):

    # example state machine:

    

    # state = "START"

    if (state == "START"):
        state = start()
    if (state == "STOP"):
        state = stop()
    if (state == "leftTurn"):
        state = LT()
    if (state == "threadNeedle"):
        state = TN()
    if (state == "rightTurn"):
        state = RT()
    if (state == "straightOn"):
        state = SO()

    


    #ex drive code
    """
    if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
        robot.move(sped,sped)
    else:
        if (isColorInSplit(camera[0], yellow) == False and isColorInSplit(camera[1], yellow) == False and isColorInSplit(camera[2], yellow) == False):
            if (isColorInSplit(camera[0], red) == False and isColorInSplit(camera[1], red) == False and isColorInSplit(camera[2], red) == False):
                #turn left arround blue barrels
                if (isColorInSplit(camera[0], blue) == True):
                    is_blue = True
                    robot.move(sped,sped)
                    #if (isColorInSplit(camera[1], blue) == True):

                elif (is_blue == True and isColorInSplit(camera[1], blue) == False):
                    robot.constantRotate(-sped)
                elif (isColorInSplit(camera[1], blue) == True):
                    robot.constantRotate(sped)
                else:
                    robot.move(sped,sped)    
            else:
                if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
                    robot.move(sped,sped)
                    #pass
                else:
                    #camera = cameraData['main']
                    if (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True):     #if red in left and right
                        robot.move(sped,sped)                                                                       #go straight
                    #elif (isColorInSplit(camera[1], red) == True):
                        #robot.move(30,30)
                    elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == False):  #if red in left and not in right
                        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                            robot.move(sped,sped)                                                                   #go forward
                        #if ()
                        robot.constantRotate(-sped)                                                               #turn left
                    elif (isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == True):  #if red not in left and in right
                        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                            robot.move(sped,sped)                                                                   #go forward
                        robot.constantRotate(sped)                                                                #turn right
                    #elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True and isColorInSplit(camera[1], red) == True):    #if all red
                        #robot.move(150,150)                                                                     #go straight
                    elif (isColorInSplit(camera[1], red) == True):                                              #if red mid and not left or right
                        robot.move(sped,sped)                                                                     #go straight
                    if (isColorInSplit(camera[1], red) == True and isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == False) :
                        robot.move(sped,sped)                                                                     #go straight

        else:
            if (isColorInSplit(camera[0], yellow) == True):
                is_yellow = True
                robot.move(sped,sped)
                #if (isColorInSplit(camera[1], blue) == True):

            elif (is_yellow == True and isColorInSplit(camera[1], yellow) == False):
                robot.constantRotate(sped)
            elif (isColorInSplit(camera[1], yellow) == True):
                robot.constantRotate(-sped)
            else:
                robot.move(sped,sped) 
    """
    #end of ex drive code





"""
    if (isColorInSplit(camera[0], yellow) == True):
        is_yellow = True
        robot.move(30,30)
        #if (isColorInSplit(camera[1], blue) == True):

    elif (is_yellow == True and isColorInSplit(camera[1], yellow) == False):
        robot.constantRotate(30)
    elif (isColorInSplit(camera[1], yellow) == True):
        robot.constantRotate(-30)
    else:
        robot.move(30,30)    
"""
"""
    if (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True):     #if red in left and right
        robot.move(30,30)                                                                       #go straight
    #elif (isColorInSplit(camera[1], red) == True):
        #robot.move(30,30)
    elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == False):  #if red in left and not in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            robot.move(30,30)                                                                   #go forward
        robot.constantRotate(-30)                                                               #turn left
    elif (isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == True):  #if red not in left and in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            robot.move(30,30)                                                                   #go forward
        robot.constantRotate(30)                                                                #turn right
    elif (isColorInSplit(camera[1], red) == True):
        robot.move(30,30)
"""
    
            
    #for object in camera[1]:
        
    #for object in camera[2]:
        #print("]")
        #print(split)
"""
        if object['color'] in camera[2] == blue or object['color'] in camera[1] == blue:
            robot.rotate(30,10)
        elif object['color'] in camera[0] == blue:
            is_blue = True
            robot.move(30,30)
        elif is_blue:
            robot.rotate(-30,10)
        else:
            robot.move(30,30)
"""
            


        
        #if(robot.getAngle() < 180):
            #robot.rotate(120, 182-robot.getAngle())
        # if(robot.isNotMoving()):
        #     robot.constantMove(60)
        #     robot.constantRotate(40)


        
    
    # if (sensorData['Front'] < 100 and sensorData['Front'] != -1):
    #     while (mod == 0):
    #         mod = random.randrange(-1,2)
    #     robot.rotate(700 * mod, 35)
    # elif (robot.isNotMoving()):
    #     mod = 0
    #     robot.constantMove(400)

def keyboard(events):
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            robot.rotate(90, 45)


# Pixels is the resolution on screen
# Course resolution is the grid count used to draw a course
course = robot_sim.Course(pixelsX=1000,
                          pixelsY=800,
                          courseResolutionX=220,
                          courseResolutionY=180)


# -- Draw course --
course.createOuterWalls(c=white)

course.circle(x=40, y=30, r=2, c=blue)
course.circle(x=40,y=140,r=2,c=blue)
course.circle(x=170,y=30,r=2,c=blue)
course.circle(x=170,y=140,r=2,c=blue)

course.circle(x =107,y=120,r=2,c=yellow)

course.circle(x=107,y=10,r=2,c=red)
course.circle(x=107,y=20,r=2,c=red)

course.circle(x=30, y=70, r=2, c=green)


# course.circle(x = 90, y=120, r=2, c=yellow)





#course.box(x1=150,y1=10,x2=160,y2=180,c=green)
#course.box(x1=30,y1=150,x2=40,y2=40,c=red)



# Sensors:
#                 | 0°
#                 |
#            __________
#     -90°  |          |
#    -------S <- (x,y) |
#    |--d---|          |
#           |          |
#           |  Robot   |
#           |          |
#           |          |
#      (0,0)x----------
#
sensors = {
    "L": robot_sim.Sensor(x=0,y=19,d=300,angle=-90,debug=True),
    "L45": robot_sim.Sensor(x=0,y=19,d=300,angle=-45,debug=True),
    "R": robot_sim.Sensor(x=9,y=19,d=300,angle=90,debug=True),
    "R45": robot_sim.Sensor(x=9,y=19,d=300,angle=45,debug=True),
    "Front": robot_sim.Sensor(x=4.5,y=19,d=300,angle=0,debug=True)
}

# Cameras:
#                 | 0°
#                 |
#            ___________
#           |           |
#           | \       / |
#           |  \     /  |
#           |   \   /   |
#           |    \ϴ/ <---- fieldOfView
#           |     C     |
#           |   (x,y)   |
#      (0,0)x-----------
#
cameras = {
    'main': robot_sim.Camera(x=4.5,
                   y=9.5,
                   angle=0,
                   fieldOfView=90,
                   splitCount=3, # How many splits are in the camera when showing object colors
                   resolution=40, # How many rays are in the field of view
                   debug=True,
                   maxDistance=300
                   )
}

# Location is pixel placement in display
# Length and width are in pixels
robot = robot_sim.RobotSim(location=(850,400),
                           length=19,
                           width=9,
                           algorithm=algorithm,
                           sensors=sensors,
                           cameras=cameras,
                           debugPrint=True)

robot_sim.run(course, robot, FPS)
















#state = {"leftTurn", "straightOn", "rightTurn", "threadNeedle", "hop", "undefined"}
"""
def start():
    #do stuff
    return "STOP"

def stop():
    return "START"

def LT():
    if (isColorInSplit(camera[0], red) == True or
    isColorInSplit(camera[1], red) == True or
    isColorInSplit(camera[2], red) == True):
        return "threadNeedle"
    if (isColorInSplit(camera[2], yellow) == True):
        return "rightTurn"
    #turn left arround blue barrels
    if (isColorInSplit(camera[0], blue) == True):
        is_blue = True
        robot.move(sped,sped)
        #if (isColorInSplit(camera[1], blue) == True):
    elif (is_blue == True and isColorInSplit(camera[1], blue) == False):
        robot.constantRotate(-sped)
    elif (isColorInSplit(camera[1], blue) == True):
        robot.constantRotate(sped)
    else:
        robot.move(sped,sped)    
    return "rightTurn"

def TN():
    if (isColorInSplit(camera[0], blue) == True or
    isColorInSplit(camera[1], blue) == True or
    isColorInSplit(camera[2], blue) == True):
        return "rightTurn"
    if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
        return "straightOn"
    if (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True):     #if red in left and right
        robot.move(sped,sped)                                                                       #go straight
    #elif (isColorInSplit(camera[1], red) == True):
        #robot.move(30,30)
    elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == False):  #if red in left and not in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            robot.move(sped,sped)                                                                   #go forward
        #if ()
        robot.constantRotate(-sped)                                                               #turn left
    elif (isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == True):  #if red not in left and in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            robot.move(sped,sped)                                                                   #go forward
        robot.constantRotate(sped)                                                                #turn right
    #elif (isColorInSplit(camera[0], red) == True and isColorInSplit(camera[2], red) == True and isColorInSplit(camera[1], red) == True):    #if all red
        #robot.move(150,150)                                                                     #go straight
    elif (isColorInSplit(camera[1], red) == True):                                              #if red mid and not left or right
        robot.move(sped,sped)                                                                     #go straight
    if (isColorInSplit(camera[1], red) == True and isColorInSplit(camera[0], red) == False and isColorInSplit(camera[2], red) == False) :
        robot.move(sped,sped)
    return "threadNeedle"

def RT():
    if (isColorInSplit(camera[0], blue)):
        return "leftTurn"
    if (isColorInSplit(camera[0], yellow) == True):
        is_yellow = True
        robot.move(sped,sped)
        #if (isColorInSplit(camera[1], blue) == True):

    elif (is_yellow == True and isColorInSplit(camera[1], yellow) == False):
        robot.constantRotate(sped)
    elif (isColorInSplit(camera[1], yellow) == True):
        robot.constantRotate(-sped)
    else:
        robot.move(sped,sped)
    return "rightTurn"

def SO():
    if (isColorInSplit(camera[0], blue) == True or
    isColorInSplit(camera[1], blue) == True or
    isColorInSplit(camera[2], blue) == True):
        return "leftTurn"
    if (isColorInSplit(camera[0], red) == True or
    isColorInSplit(camera[1], red) == True or
    isColorInSplit(camera[2], red) == True):
        return "threadNeedle"
    if (isColorInSplit(camera[0], red) == False or
    isColorInSplit(camera[1], red) == False or
    isColorInSplit(camera[2], red) == False):
        return "rightTurn"
    robot.move(sped,sped)
    return "straightOn"

# example state machine:

state = "straightOn"

# state = "START"

if (state == "START"):
    state = start()
if (state == "STOP"):
    state = stop()
if (state == "leftTurn"):
    state = LT()
if (state == "threadNeedle"):
    state = TN()
if (state == "rightTurn"):
    state = RT()
if (state == "straightOn"):
    state = SO()
"""











