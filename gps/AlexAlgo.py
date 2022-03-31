from operator import truediv
import run

distanceErr = .5
courseErr = 15.0
moveSpeed = 10.0
moveDist = .5
rotSpeed = 180
rotDist = 15

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
        return ((course % 360) > (180 - courseErr) or (course % 360) < (0 + courseErr))

def checkState(distances, cameraObjects, position, course, state):
    #changes state once certain conditions are met
    if state == None:
        state = "Straight 1"
    if state == "Straight 1":
        if not isColorPresent(cameraObjects, "Front", "Blue")[0]:
            return "Turn 1"
        else:
            return state
    if state == "Turn 1":
        print(course)
        if isColorPresent(cameraObjects, "Front", "Yellow")[0] or course > (315 + courseErr):
            return "Yellow"
        else:
            return state
        
    

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
        
#Algorithm
def algo(robot, t, events=None):
    global state

    distances = robot.getSensorData()
    cameraObjects = robot.getCameraData()["main"]
    position = robot.getPosition()
    course = robot.getAngle()

    #Crash Prevention <3
    if distances["Front"] < .5:
        robot.stop()
        
    state = checkState(distances, cameraObjects, position, course, state)

    #Straight 1
    if(state == "Straight 1" or state == "Turn 1"):
        #Correct heading
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if(isColorPresent(cameraObjects, "Front", "Blue")[0]):
                 robot.rotate(-rotSpeed, 5)
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
        print("Time to Turn!!!")

    if state == "Yellow":
        print("Done!!")







run.algo = algo
#run.isSim = False
run.run()