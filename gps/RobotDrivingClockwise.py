#import robot_sim
#import robot
import random
#import pygame
#import Roomba
import run

isSim2 = True
white = "White"
blue = "Blue"
green = "Green"
red = "Red"
yellow = "Yellow"

# Target FPS
FPS = 60
flip = False

mod = 0
flag = 0
is_blue = False
is_yellow = False
rightRed = False
leftRed = False
greenRight = False
greenLeft = False
leftSense = False
rightSense = False
sped = .5
rotateSped = 720
rotRad = 10
rotDist = 10
blueExitAng = 100
yellowExitAng = 30
angleOnBlueEntry = 0
angleOnYellowEntry = 0
useAngles = True
startAngle = 0
state = "START"
"""
if (isSim2 == True):                     #set initial conditions for simulation 
    white = (255,255,255,255)
    blue = (0,0,255,255)
    green = (0,255,0,255)
    red = (255,0,0,255)
    yellow = (255, 255 , 0, 255)
    sped = 150
"""

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
    global greenRight
    global greenLeft
    global leftSense
    global rightSense
    global rotateSped
    global rotRad
    global rotDist
    global blueExitAng
    global angleOnBlueEntry
    global angleOnYellowEntry
    global useAngles
    global startAngle

    print(state)
    # 'events' from pygame
    # 'time' time since start of program in seconds
    sensorData = robot.getSensorData()
    cameraData = robot.getCameraData()
    #keyboard(events)
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
    if (isColorInSplit(camera[2], blue) == False):
        if (isColorInSplit(camera[1], blue) == False):
            if (is_blue == True):
                robot.constantRotate(-30)
            else:
                is_blue = False
    else:
        is_blue = True
    if (isColorInSplit(camera[0], yellow) == False):
        if (isColorInSplit(camera[1], yellow) == False):
            if (is_yellow == True):
                robot.constantRotate(30)
        is_yellow = False
    else:
        is_yellow = True
    robot.move(30,30)
    """
    def angleMagnitude():
        variable = robot.getAngle()
        #if (variable < 0):
        #    variable = variable * -1
        #    variable = variable + 180
        variable = variable + 180
        return variable

    def leftTurn():
        robot.constantRotate(rotateSped)
        #robot.arcMove(rotateSped, rotRad, rotDist)
        return

    def rightTurn():
        robot.constantRotate(-rotateSped)
        #robot.arcMove(-rotateSped, rotRad, rotDist)
        return

    def goForward():
        robot.move(sped, sped)
        return

    def start():
        #do stuff
        startAngle = robot.initAngle()
        startAngle = robot.initialAngle
        robot.initAngle()
        #algo(robot, time, events)
        #return "straightOn"
        return "threadNeedle"
        return "STOP"

    def stop():
        return "START"

    def checkToLeaveBlue(angleOnBlueEntry):
        global is_blue
        global blueExitAng
        if ((isColorInSplit(camera[2], blue) == True or is_blue == True) and (sensorData['Right'] < 100 and sensorData['Right'] != -1)):
            goForward()
            return "blueTurn"
        if (isColorInSplit(camera[2], red) == True or
        isColorInSplit(camera[1], red) == True or
        isColorInSplit(camera[0], red) == True):
            return "straightOn"
        if (isColorInSplit(camera[0], yellow) == True):
            goForward()    
            return "straightOn"
        if (isColorInSplit(camera[1], green) == True):
            return "jump"
        if (useAngles == True):
            tempAng = angleMagnitude()
            
            if (tempAng > 360 and (isColorInSplit(camera[2], blue) == False)):
                blueExitAng = 100
                is_blue = False
                goForward()
                return "straightOn"
            overflowProtection = angleOnBlueEntry + blueExitAng
            if (overflowProtection > 360):
                overflowProtection = overflowProtection - 360
                if (tempAng > 90 and tempAng < 180):
                    is_blue = False
                    goForward()
                    return "straightOn"
            elif (tempAng > (overflowProtection) and (isColorInSplit(camera[2], blue) == False)):
                is_blue = False
                goForward()
                return "straightOn"
                #if (robot.getAngle() == 0 and is_blue == False):
        #return "straightOn"
        return "no"

    def turnRoundBlue(angleOnBlueEntry):
        global is_blue
        #turn left arround blue barrels
        if (isColorInSplit(camera[2], blue) == True):
            is_blue = True
            goForward()
            #if (isColorInSplit(camera[1], blue) == True):
        elif (is_blue == True and isColorInSplit(camera[1], blue) == False):
            #robot.constantRotate(-sped)
            #robot.Rotoate(-rotateSped)
            #rightTurn()
            leftTurn()
        elif (isColorInSplit(camera[1], blue) == True or (isColorInSplit(camera[0], blue) == True) ):
            #robot.constantRotate(sped)
            #robot.constantRotate(rotateSped)
            #leftTurn()
            rightTurn()
        else:
            goForward()   
        return "no"

    def BlueTurn():
        global is_blue
        global angleOnBlueEntry
        leave = checkToLeaveBlue(angleOnBlueEntry)
        if(leave == "no"):
            turnRoundBlue(angleOnBlueEntry)
            return "blueTurn"
        else:
            return leave
        return "blueTurn"

    def checkToLeaveThreadNeedle():
        global leftRed
        global rightRed
        global leftSense
        global rightSense
        if (isColorInSplit(camera[2], blue) == True or
        isColorInSplit(camera[1], blue) == True or
        isColorInSplit(camera[0], blue) == True):
            leftSense = False
            rightSense = False
            leftRed = False
            rightRed = False
            return "blueTurn"
        if (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True and isColorInSplit(camera[1], red) == False):
            goForward()      
            return "threadNeedle"
        if (sensorData['Left'] < 15 and sensorData['Left'] != -1):
            leftSense = True
        if (sensorData['Right'] < 15 and sensorData['Right'] != -1):
            rightSense = True
        if (leftSense == True and rightSense == True):
            leftSense = False
            rightSense = False
            return "straightOn"
        if (sensorData['Left'] < 100 and sensorData['Left'] != -1 and sensorData['Right'] < 100 and sensorData['Right'] != -1):
            goForward()
            leftSense == False
            rightSense == False
            return "straightOn"
        return "no"

    def goThrough():
        global leftRed
        global rightRed
        global leftSense
        global rightSense
        if (sensorData['FrontLeft'] < 50 and sensorData['FrontRight'] > 50):
            #robot.constantRotate(sped)
            leftTurn()
        if (sensorData['FrontLeft'] > 50 and sensorData['FrontRight'] < 50):
            #robot.constantRotate(-sped)
            rightTurn()
        if(sensorData['FrontLeft'] > sensorData['FrontRight'] and sensorData['FrontLeft'] < 55 and sensorData['FrontRight'] < 55):
            #robot.constantRotate(-sped)
            rightTurn()
        if(sensorData['FrontLeft'] < sensorData['FrontRight'] and sensorData['FrontLeft'] < 55 and sensorData['FrontRight'] < 55):
            #robot.constantRotate(sped)
            leftTurn()
        if(sensorData['Front'] > 75):
            goForward()
        if (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True):     #if red in left and right
            goForward()                                                                      #go straight
        #elif (isColorInSplit(camera[1], red) == True):
            #robot.move(30,30)
        elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == False and rightRed == False):  #if red in left and not in right and wasnt in right last time
            if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                goForward()                                                                  #go forward
            #if ()
            #robot.constantRotate(-sped)      
            leftTurn()                                                         #turn left
        elif (isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == True and leftRed == False):  #if red not in left and in right and wasnt in left last time
            if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                goForward()                                                                  #go forward
            #robot.constantRotate(sped) 
            rightTurn()                                                               #turn right
        #elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True and isColorInSplit(camera[1], red) == True):    #if all red
            #robot.move(150,150)                                                                     #go straight
        elif (isColorInSplit(camera[1], red) == True):                                              #if red mid and not left or right
            goForward()                                                                    #go straight
        if (isColorInSplit(camera[1], red) == True and isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == False) :
            robot.move(sped,sped)
        if (isColorInSplit(camera[2], red) == True):
            leftRed = True
        if (isColorInSplit(camera[0], red) == True):
            rightRed = True
        return

    def ThreadNeedle():
        global leftRed
        global rightRed
        global leftSense
        global rightSense
        #leave = checkToLeaveThreadNeedle()
        #if(leave == "no"):
        #    goThrough()
        #    return "threadNeedle"
        #else:
        #    return leave
        return "threadNeedle"

    def checkToLeaveYellow(angleOnYellowEntry):
        global is_yellow
        global blueExitAng
        global angleOnBlueEntry
        #if (is_blue == True and ):
            #return "straightOn"
        if ((isColorInSplit(camera[0], yellow) == True or is_yellow == True) and (sensorData['Left'] < 100 and sensorData['Left'] != -1)):
            goForward()

            return "yellowTurn"
        #if (isColorInSplit(camera[2], blue)):
            #blueExitAng = 170
            #angleOnBlueEntry = angleMagnitude()
            #return "blueTurn"
        if (useAngles == True):
            tempAng = angleMagnitude()
            #if (tempAng > (angleOnYellowEntry + yellowExitAng)):
            if (tempAng < (angleOnYellowEntry - yellowExitAng)):
                #blueExitAng = 170
                goForward()
                return "straightOn"
        return "no"

    def turnRoundYellow():
        global is_yellow
        if (isColorInSplit(camera[0], yellow) == True):
            is_yellow = True
            robot.move(sped,sped)
            #if (isColorInSplit(camera[1], blue) == True):

        elif (is_yellow == True and isColorInSplit(camera[1], yellow) == False):
            #robot.constantRotate(sped)
            rightTurn()
        elif (isColorInSplit(camera[1], yellow) == True or isColorInSplit(camera[2], yellow) == True):
            #robot.constantRotate(-sped)
            leftTurn()
        else:
            robot.move(sped,sped)
        return

    def YellowTurn():
        global is_yellow
        global angleOnYellowEntry
        leave = checkToLeaveYellow(angleOnYellowEntry)
        if (leave == "no"):
            turnRoundYellow()
            return "yellowTurn"
        else:
            return leave
        return
        return "rightTurn"

    def checkBlue():
        global is_blue
        global angleOnBlueEntry
        if (is_blue == False):
            if (isColorInSplit(camera[2], blue) == True or
            isColorInSplit(camera[1], blue) == True or
            isColorInSplit(camera[0], blue) == True):
                if (isColorInSplit(camera[2], blue) == True):
                    is_blue = True
                angleOnBlueEntry = angleMagnitude()
                return "blueTurn"
        else:
            if (isColorInSplit(camera[2], blue) == False):
                is_blue = False
        if (isColorInSplit(camera[2], blue) == False):
            is_blue = False            
        return "no"

    def checkSurrounded():
        if ((sensorData['Left'] < 100 and sensorData['Left'] != -1 and sensorData['Right'] < 100 and sensorData['Right'] != -1)):
            goForward()
            return "straightOn"
        return "no"

    def checkRed():
        global leftRed
        global rightRed
        if (leftRed == False and rightRed == False):

            if (isColorInSplit(camera[2], red) == True or
            isColorInSplit(camera[1], red) == True or
            isColorInSplit(camera[0], red) == True):
                return "threadNeedle"
        else:  
            if (isColorInSplit(camera[2], red) == False):
                leftRed = False
            if (isColorInSplit(camera[0], red) == False):
                rightRed = False
        return "no"

    def checkYellow():
        if (isColorInSplit(camera[2], yellow) == True or
        isColorInSplit(camera[1], yellow) == True):
        #or isColorInSplit(camera[0], yellow) == True):
            global angleOnYellowEntry
            angleOnYellowEntry = angleMagnitude()
            return "yellowTurn"
        else:
            is_yellow = False
        
        return "no"

    def StraightOn():
        global leftRed
        global rightRed
        global is_blue
        
        blueChecked = checkBlue()
        if (blueChecked != "no"):
            return blueChecked

        surroundedChecked = checkSurrounded()
        if (surroundedChecked != "no"):
            return surroundedChecked

        redChecked = checkRed()
        if (redChecked != "no"):
            return redChecked

        yellowChecked = checkYellow()
        if (yellowChecked != "no"):
            return yellowChecked
        #if (isColorInSplit(camera[2], green) == True or
        #isColorInSplit(camera[1], green) == True or
        #isColorInSplit(camera[0], green) == True):
            #return "greenBeam"
        robot.move(sped,sped)
        return "straightOn"

    def checkToLeaveJump():
        global greenRight
        global greenLeft
        if (isColorInSplit(camera[2], green) == False and isColorInSplit(camera[1], green) == False and isColorInSplit(camera[0], green) == False):
            greenRight = False
            greenLeft = False
            return "straightOn"
        return "no"

    def goOverJump():
        global greenRight
        global greenLeft
        if (sensorData['Front'] < 20 and sensorData['Front'] != -1 and (isColorInSplit(camera[1], green) == True)):
            greenRight = False
            greenLeft = False
            robot.move(sped,sped)
            #return "straightOn"
            #return "straightOn"
        else:
        #if (isColorInSplit(camera[1], green) == True):
        #    robot.move(sped,sped)
            if (isColorInSplit(camera[2], blue) and (sensorData['Left'] > 100)):  #and is_blue == False
                greenRight = False
                greenLeft = False
                return "blueTurn"
            if ((isColorInSplit(camera[2], green) == True or isColorInSplit(camera[0], green) == True)
                and not (isColorInSplit(camera[2], green) == True and isColorInSplit(camera[0], green) == True)):
                if (isColorInSplit(camera[2], green) == True and greenLeft == False):
                    #robot.constantRotate(-sped)
                    rightTurn()
                    greenRight = True
                    #break
                elif (isColorInSplit(camera[0], green) == True and greenRight == False):
                    #robot.constantRotate(sped)
                    leftTurn()
                    greenLeft = True
                else:
                    robot.move(sped,sped)
                #if (isColorInSplit(camera[2], green) == True):
                #    greenRight = False
                #if (isColorInSplit(camera[0], green) == True):
                #    greenRight = True
            #if (sensorData['Front'] < 10 and sensorData['Front'] != -1):
            #    return "straightOn"
            else:
                robot.move(sped,sped)
        return "no"

    def Jump():
        global greenRight
        global greenLeft

        leave = checkToLeaveJump()
        if (leave != "no"):
            return leave
        leave2 = goOverJump()
        if (leave != "no"):
            return leave
        return "jump"

    # example state machine:

    

    # state = "START"

    if (state == "START"):
        state = start()
    if (state == "STOP"):
        state = stop()
    if (state == "blueTurn"):
        state = BlueTurn()
    if (state == "threadNeedle"):
        state = ThreadNeedle()
    if (state == "yellowTurn"):
        state = YellowTurn()
    if (state == "jump") :
        state = Jump()    
    if (state == "straightOn"):
        state = StraightOn()
    

    


    #ex drive code
    """
    if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
        robot.move(sped,sped)
    else:
        if (isColorInSplit(camera[2], yellow) == False and isColorInSplit(camera[1], yellow) == False and isColorInSplit(camera[0], yellow) == False):
            if (isColorInSplit(camera[2], red) == False and isColorInSplit(camera[1], red) == False and isColorInSplit(camera[0], red) == False):
                #turn left arround blue barrels
                if (isColorInSplit(camera[2], blue) == True):
                    is_blue = True
                    robot.move(sped,sped)
                    #if (isColorInSplit(camera[1], blue) == True):

                elif (is_blue == True and isColorInSplit(camera[1], blue) == False):
                    robot.constantRotate(-sped)
                elif (isColorInSplit(camera[1], blue) == True):
                    robot.constantRotate(sped)
                else:
                    goForward()   
            else:
                if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
                    robot.move(sped,sped)
                    #pass
                else:
                    #camera = cameraData['main']
                    if (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True):     #if red in left and right
                        goForward()                                                                      #go straight
                    #elif (isColorInSplit(camera[1], red) == True):
                        #robot.move(30,30)
                    elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == False):  #if red in left and not in right
                        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                            goForward()                                                                  #go forward
                        #if ()
                        robot.constantRotate(-sped)                                                               #turn left
                    elif (isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == True):  #if red not in left and in right
                        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
                            goForward()                                                                  #go forward
                        robot.constantRotate(sped)                                                                #turn right
                    #elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True and isColorInSplit(camera[1], red) == True):    #if all red
                        #robot.move(150,150)                                                                     #go straight
                    elif (isColorInSplit(camera[1], red) == True):                                              #if red mid and not left or right
                        goForward()                                                                    #go straight
                    if (isColorInSplit(camera[1], red) == True and isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == False) :
                        goForward()                                                                    #go straight

        else:
            if (isColorInSplit(camera[2], yellow) == True):
                is_yellow = True
                robot.move(sped,sped)
                #if (isColorInSplit(camera[1], blue) == True):

            elif (is_yellow == True and isColorInSplit(camera[1], yellow) == False):
                robot.constantRotate(sped)
            elif (isColorInSplit(camera[1], yellow) == True):
                robot.constantRotate(-sped)
            else:
                goForward()
    """
    #end of ex drive code





"""
    if (isColorInSplit(camera[2], yellow) == True):
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
    if (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True):     #if red in left and right
        robot.move(30,30)                                                                       #go straight
    #elif (isColorInSplit(camera[1], red) == True):
        #robot.move(30,30)
    elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == False):  #if red in left and not in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            robot.move(30,30)                                                                   #go forward
        robot.constantRotate(-30)                                                               #turn left
    elif (isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == True):  #if red not in left and in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            robot.move(30,30)                                                                   #go forward
        robot.constantRotate(30)                                                                #turn right
    elif (isColorInSplit(camera[1], red) == True):
        robot.move(30,30)
"""
    
            
    #for object in camera[1]:
        
    #for object in camera[0]:
        #print("]")
        #print(split)
"""
        if object['color'] in camera[0] == blue or object['color'] in camera[1] == blue:
            robot.rotate(30,10)
        elif object['color'] in camera[2] == blue:
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
"""
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
"""
"""
if (isSim2 == True): 
    import robot_sim                                                     #if in the simultaion mode
    # Pixels is the resolution on screen
    # Course resolution is the grid count used to draw a course
    course = robot_sim.Course(pixelsX=1000,
                            pixelsY=800,
                            courseResolutionX=220,
                            courseResolutionY=180)


    # -- Draw course --
    #course.createOuterWalls(c=white)

    course.circle(x=40, y=30, r=2, c=blue)
    course.circle(x=40,y=140,r=2,c=blue)
    course.circle(x=170,y=30,r=2,c=blue)
    course.circle(x=170,y=140,r=2,c=blue)

    course.circle(x =107,y=120,r=2,c=yellow)

    course.circle(x=107,y=10,r=2,c=red)
    course.circle(x=107,y=20,r=2,c=red)

    course.circle(x=30, y=70, r=2, c=green)
    course.circle(x=180, y=80, r=2, c=green)

    # course.circle(x = 90, y=120, r=2, c=yellow)
#True



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
        "Left": robot_sim.Sensor(x=0,y=19,d=300,angle=-90,debug=True),
        "FrontLeft": robot_sim.Sensor(x=0,y=19,d=300,angle=-45,debug=True),
        "Right": robot_sim.Sensor(x=9,y=19,d=300,angle=90,debug=True),
        "FrontRight": robot_sim.Sensor(x=9,y=19,d=300,angle=45,debug=True),
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
    robot = robot_sim.RobotSim(location=(700,325),          #
                            length=19,
                            width=9,
                            algorithm=algorithm,#Roomba.run,
                            sensors=sensors,
                            cameras=cameras)

    robot_sim.run(course, robot, FPS)
#end of simulation specific stuff
else:
    import robot
    while(True):
        robot.tick()
"""








#state = {"leftTurn", "straightOn", "rightTurn", "threadNeedle", "hop", "undefined"}
"""
def start():
    #do stuff
    return "STOP"

def stop():
    return "START"

def LT():
    if (isColorInSplit(camera[2], red) == True or
    isColorInSplit(camera[1], red) == True or
    isColorInSplit(camera[0], red) == True):
        return "threadNeedle"
    if (isColorInSplit(camera[0], yellow) == True):
        return "rightTurn"
    #turn left arround blue barrels
    if (isColorInSplit(camera[2], blue) == True):
        is_blue = True
        robot.move(sped,sped)
        #if (isColorInSplit(camera[1], blue) == True):
    elif (is_blue == True and isColorInSplit(camera[1], blue) == False):
        robot.constantRotate(-sped)
    elif (isColorInSplit(camera[1], blue) == True):
        robot.constantRotate(sped)
    else:
        goForward()   
    return "rightTurn"

def TN():
    if (isColorInSplit(camera[2], blue) == True or
    isColorInSplit(camera[1], blue) == True or
    isColorInSplit(camera[0], blue) == True):
        return "rightTurn"
    if (sensorData['L'] < 100 and sensorData['L'] != -1 and sensorData['R'] < 100 and sensorData['R'] != -1):
        return "straightOn"
    if (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True):     #if red in left and right
        goForward()                                                                      #go straight
    #elif (isColorInSplit(camera[1], red) == True):
        #robot.move(30,30)
    elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == False):  #if red in left and not in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            goForward()                                                                  #go forward
        #if ()
        robot.constantRotate(-sped)                                                               #turn left
    elif (isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == True):  #if red not in left and in right
        if (isColorInSplit(camera[1], red) == True):                                            #if red in mid + ^
            goForward()                                                                  #go forward
        robot.constantRotate(sped)                                                                #turn right
    #elif (isColorInSplit(camera[2], red) == True and isColorInSplit(camera[0], red) == True and isColorInSplit(camera[1], red) == True):    #if all red
        #robot.move(150,150)                                                                     #go straight
    elif (isColorInSplit(camera[1], red) == True):                                              #if red mid and not left or right
        goForward()                                                                    #go straight
    if (isColorInSplit(camera[1], red) == True and isColorInSplit(camera[2], red) == False and isColorInSplit(camera[0], red) == False) :
        robot.move(sped,sped)
    return "threadNeedle"

def RT():
    if (isColorInSplit(camera[2], blue)):
        return "leftTurn"
    if (isColorInSplit(camera[2], yellow) == True):
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
    if (isColorInSplit(camera[2], blue) == True or
    isColorInSplit(camera[1], blue) == True or
    isColorInSplit(camera[0], blue) == True):
        return "leftTurn"
    if (isColorInSplit(camera[2], red) == True or
    isColorInSplit(camera[1], red) == True or
    isColorInSplit(camera[0], red) == True):
        return "threadNeedle"
    if (isColorInSplit(camera[2], red) == False or
    isColorInSplit(camera[1], red) == False or
    isColorInSplit(camera[0], red) == False):
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

def algo(robot, time, test):
    robot.initAngle()
    print(robot.getAngle())


run.algo = algorithm

run.run()







