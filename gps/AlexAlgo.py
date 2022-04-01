import run

distanceErr = .5
courseErr = 15.0
moveSpeed = 10.0
moveDist = .5
rotSpeed = 270
rotDist = 5

state = "Straight 1"

splitDict = {
    "Left":0,
    "Front":1,
    "Right":2
    }

#State
def isCorrectHeading(distances, cameraObjects, position, course, state):
    global courseErr
    #Returns a guess of where it thinks the robot is. Should match stored state
    #Straight 1
    if state == "Straight 1":
        return ((course % 360) > (180 - courseErr) and (course % 360) < (180 + courseErr))
    if state == "Turn 1":
        return ((course % 360) > (180 - courseErr) and (course % 360) < (300 + courseErr))
    if state == "Yellow":
        return ((course % 360) > (180 - courseErr) and (course % 360) < (340 + courseErr))
    if state == "Straight 2":
        return ((course % 360) > (180 - courseErr) and (course % 360) < (270 + courseErr))
    if state == "Turn 2":
        return ((course % 360) > (180 - courseErr) or (course % 360) < (0 + courseErr))
    if state == "Straight 3":
        return ((course % 360) > (360 - courseErr) or (course % 360) < (0 + courseErr))
    if state == "Turn 3":
        return ((course % 360) > (360 - courseErr) or (course % 360) < (90 + courseErr))
    if state == "Tunnel":
        return ((course % 360) > (85 - courseErr) and (course % 360) < (85 + courseErr))
    if state == "Straight 4":
        return ((course % 360) > (70 - courseErr) and (course % 360) < (90 + courseErr))
    if state == "Turn 4":
        return ((course % 360) > (90 - courseErr) and (course % 360) < (180 + courseErr))
    if state == "Straight 5":
        return ((course % 360) > (180 - courseErr) and (course % 360) < (180 + courseErr))

def checkState(distances, cameraObjects, position, course, state):
    #changes state once certain conditions are met
    if state == None:
        print("state was None")
        state = "Straight 1"

    if state == "Straight 1":
        if not isColorPresent(cameraObjects, "Front", "Blue")[0] and course < (315 + courseErr):
            return "Turn 1"
        else:
            return state

    if state == "Turn 1":
        print(course)
        if isColorPresent(cameraObjects, "Front", "Yellow")[0] or course > (300 + courseErr):
            return "Find Yellow"
        else:
            return state

    if state == "Find Yellow":
        print("Searching for Yellow")
        if isColorPresent(cameraObjects, "Left", "Yellow")[0]:
            return "Yellow"
        else:
            return state
    
    if state == "Yellow":
        if not (course % 360) > 255 - courseErr:
            return "Find Blue 1"
        else:
            return state

    if state == "Find Blue 1":
        print("Searching for Blue 1")
        if isColorPresent(cameraObjects, "Right", "Blue")[0]:
            return "Straight 2"
        else:
            return state
    
    if state == "Straight 2":
        if not isColorPresentAtAll(cameraObjects, "Blue")[0] and (course % 360) < (235 + courseErr):
            return "Turn 2"
        else:
            return state

    if state == "Turn 2":
        print(course % 360)
        if (course % 360) > 10 - courseErr and (course % 360) < 20 + courseErr:
            return "Find Blue 2"
        else:
            return state

    if state == "Find Blue 2":
        print("Searching for Blue 2")
        if isColorPresent(cameraObjects, "Right", "Blue")[0]:
            return "Straight 3"
        else:
            return state
    
    if state == "Straight 3":
        if not isColorPresentAtAll(cameraObjects, "Blue")[0] and ((course % 360) > 360 - courseErr or (course % 360) < (0 + courseErr)):
            return "Turn 3"
        else:
            return state

    if state == "Turn 3":
        print(course % 360)
        if (course % 360) > 110 - courseErr and (course % 360) < 110 + courseErr:
            return "Find Red"
        else:
            return state

    if state == "Find Red":
        print("Searching for Red")
        if isColorPresentAtAll(cameraObjects, "Red")[0]:
            return "Tunnel"
        else:
            return state
    
    if state == "Tunnel":
        if not isColorPresentAtAll(cameraObjects, "Red")[0]:
            print("Should find Blue")
            return "Find Blue 3"
        else:
            return state

    if state == "Find Blue 3":
        print("Searching for Blue 3")
        if isColorPresent(cameraObjects, "Right", "Blue")[0]:
            return "Straight 4"
        else:
            return state
    
    if state == "Straight 4":
        if not isColorPresentAtAll(cameraObjects, "Blue")[0] and ((course % 360) > 70 - courseErr or (course % 360) < (90 + courseErr)):
            return "Turn 4"
        else:
            return state

    if state == "Turn 4":
        print(course % 360)
        if (course % 360) > 180 - courseErr:
            return "Straight 5"
        else:
            return state
    
    if state == "Straight 5":
        print("We're in the endgame now")
        if isColorPresent(cameraObjects, "Left", "Yellow")[0]:
            return "Finish"
        else:
            return state

    if state == "Finish":
        return "Finish"

#Position Tests

def isColorPresent(cameraObjects, splitName, color):
    global splitDict

    flag = False
    count = 0
    splitNum = splitDict[splitName]

    for o in cameraObjects[splitNum]:
        if o["color"] == color:
            flag = True
            count += 1

    return flag, count

def isColorPresentAtAll(cameraObjects, color):

    global splitDict

    flag = False
    count = 0

    for splitNum in range(len(splitDict)):
        for o in cameraObjects[splitNum]:
            if o["color"] == color:
                flag = True
                count += 1

    return flag, count

#Correction
def correctRobot(robot, distances, cameraObjects, position, course, state, correction):
    global rotSpeed
    global rotDist
    
    if state == "Straight 1":
        if correction == "Heading":
            if (course % 360) > (180 + courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
            elif (course % 360) < (180 - courseErr):
                robot.rotate(-rotSpeed, rotDist) # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Turn 1":
        if correction == "Heading":
            if (course % 360) > (0 + courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
            elif (course % 360) < (180 - courseErr):
                robot.rotate(-rotSpeed, rotDist) # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Yellow":
        if correction == "Camera":
            robot.constantRotate(-rotSpeed)

    if state == "Straight 2":
        if correction == "Heading":
            if (course % 360) > (270 + courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
            elif (course % 360) < (180 - courseErr):
                robot.rotate(-rotSpeed, rotDist) # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Turn 2":
        if correction == "Heading":
            if (course % 360) > (0 + courseErr) and (course % 360) < (90):
                robot.rotate(-rotSpeed, rotDist) # left adj
            elif (course % 360) < (180 - courseErr) and (course % 360) > (90):
                robot.rotate(rotSpeed, rotDist) # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Straight 3":
        if correction == "Heading":
            if (course % 360) < (360 - courseErr) and (course % 360) > 180:
                robot.rotate(rotSpeed, rotDist) # right adj
            elif (course % 360) > (0 + courseErr) and (course % 360) < 180:
                robot.rotate(-rotSpeed, rotDist) # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Turn 3":
        if correction == "Heading":
            if (course % 360) > (0 + courseErr) and (course % 360) < (90):
                robot.rotate(-rotSpeed, rotDist) # left adj
            elif (course % 360) < (180 - courseErr) and (course % 360) > (90):
                robot.rotate(rotSpeed, rotDist) # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Tunnel":
        if correction == "Heading":
            print("heading adj")
            if (course % 360) > (85 + courseErr):
                robot.rotate(-rotSpeed, rotDist) # left adj
            elif (course % 360) < (85 - courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
        elif correction == "Camera":
            print("camera adj")
            if isColorPresent(cameraObjects, "Left", "Red")[1] > 1:
                robot.rotate(-rotSpeed, rotDist) # left adj
            if isColorPresent(cameraObjects, "Right", "Red")[1] > 1:
                robot.rotate(rotSpeed, rotDist) # right adj
            if isColorPresent(cameraObjects, "Left", "Red")[1] == 1 and not isColorPresent(cameraObjects, "Right", "Red")[1] == 1:
                robot.constantMove(moveSpeed)
            if isColorPresent(cameraObjects, "Right", "Red")[1] == 1 and not isColorPresent(cameraObjects, "Left", "Red")[1] == 1:
                robot.constantMove(moveSpeed)

    if state == "Straight 4":
        if correction == "Heading":
            if (course % 360) > (90 + courseErr):
                robot.rotate(-rotSpeed, rotDist) # left adj
            elif (course % 360) < (90 - courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Turn 4":
        if correction == "Heading":
            if (course % 360) > (180 + courseErr):
                robot.rotate(-rotSpeed, rotDist) # left adj
            elif (course % 360) < (90 - courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj

    if state == "Straight 5":
        if correction == "Heading":
            if (course % 360) < (360 - courseErr) and (course % 360) > 180:
                robot.rotate(rotSpeed, rotDist) # right adj
            elif (course % 360) > (0 + courseErr) and (course % 360) < 180:
                robot.rotate(-rotSpeed, rotDist) # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)# right adj
        
#Algorithm
def algo(robot, t, events=None):
    global state

    distances = robot.getSensorData()
    cameraObjects = robot.getCameraData()["main"]
    position = robot.getPosition()
    course = robot.getAngle()

    # print(cameraObjects)
    print(state)

    #Crash Prevention <3
    if distances["Front"] < .5:
        robot.stop()
        
    state = checkState(distances, cameraObjects, position, course, state)

    #Straight 1
    if(state == "Straight 1"):
        #Correct heading
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if(isColorPresent(cameraObjects, "Front", "Blue")[0]):
                 robot.constantRotate(-rotSpeed)
            elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
                 robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")

    #Turn 1
    if(state == "Turn 1"):
        if (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            robot.constantMove(moveSpeed)
        else:
            print("camera adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")

    if state == "Find Yellow":
        robot.constantMove(moveSpeed)

    #Yellow
    if state == "Yellow":
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            
            if(isColorPresent(cameraObjects, "Right", "Yellow")[0] or isColorPresent(cameraObjects, "Front", "Yellow")[0]):
                robot.constantRotate(rotSpeed)
            elif(isColorPresent(cameraObjects, "Left", "Yellow")[0]):
                robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")


    if state == "Find Blue 1":
        robot.constantMove(moveSpeed)

    if state == "Straight 2":
        print("Straight 2")
        #Correct heading
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if(isColorPresent(cameraObjects, "Front", "Blue")[0]):
                 robot.constantRotate(-rotSpeed)
            elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
                 robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")


    #Turn 2
    if(state == "Turn 2"):
        if (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            robot.constantMove(moveSpeed)
        else:
            print("camera adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")


    if state == "Find Blue 2":
        robot.constantMove(moveSpeed)

    if state == "Straight 3":
        print("Straight 3")
        #Correct heading
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if(isColorPresent(cameraObjects, "Front", "Blue")[0]):
                 robot.constantRotate(-rotSpeed)
            elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
                 robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")


    #Turn 2
    if(state == "Turn 3"):
        if (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            robot.constantMove(moveSpeed)
        else:
            print("camera adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")

    if state == "Find Red":
        robot.constantMove(moveSpeed)

    if state == "Tunnel":
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if (isColorPresentAtAll(cameraObjects, "Red")):
                robot.constantMove(moveSpeed)
            elif (isColorPresent(cameraObjects, "Left", "Red")[1] == 1 and isColorPresent(cameraObjects, "Right", "Red")[1] == 1):
                robot.constantMove(moveSpeed)
            elif (isColorPresent(cameraObjects, "Front", "Red")[1] == 2):
                robot.constantMove(moveSpeed)
            else:
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")

    if state == "Find Blue 3":
        if(isColorPresent(cameraObjects, "Front", "Blue")[0] or isColorPresent(cameraObjects, "Left", "Blue")[0]):
            robot.constantRotate(-rotSpeed)
        else:
            robot.constantMove(moveSpeed)

    if state == "Straight 4":
        print("Straight 4")
        #Correct heading
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if (isColorPresent(cameraObjects, "Front", "Blue")[0]):
                robot.constantMove(moveSpeed)
            elif (isColorPresent(cameraObjects, "Left", "Blue")[0]):
                 robot.constantRotate(-rotSpeed)
            elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
                 robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")


    #Turn 2
    if(state == "Turn 4"):
        print(cameraObjects)
        print(isColorPresent(cameraObjects, "Right", "Blue")[0])
        if (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            robot.constantMove(moveSpeed)   
            print("move") 
        elif (isColorPresent(cameraObjects, "Front", "Blue")[0]):
            robot.constantMove(moveSpeed)   
            print("rot left") 
        else:
            print("camera adj")
            correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")

    if state == "Straight 5":
        robot.constantMove(moveSpeed)


run.algo = algo
#run.isSim = False
run.run()