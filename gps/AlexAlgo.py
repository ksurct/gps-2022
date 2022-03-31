import run

distanceErr = .5
courseErr = 15.0
moveSpeed = 10.0
moveDist = .5
rotSpeed = 90
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
    if ((course % 360) > (270 - courseErr) and (course % 360) > (270 + courseErr)):
        return "Straight 1"

def checkState(distances, cameraObjects, position, course, state):
    #changes state once certain conditions are met
    if state == "Straight 1":
        if distances["FrontRight"] < .5:
            return "Turn 1"
        else:
            return state
        
    

#Position Tests

def isBlue(cameraObjects, splitName):
    global splitDict

    flag = False
    count = 0
    splitNum = splitDict[splitName]

    for o in cameraObjects[splitNum]:
        if o["color"] == "Blue":
            flag = True
            count += 1

    return flag, count

#Correction
def correctRobot(robot, distances, cameraObjects, position, course, state, correction):
    global rotSpeed
    global rotDist
    
    if state == "Straight 1":
        if correction == "Heading":
            if (course % 360) > (270 + courseErr):
                robot.rotate(rotSpeed, rotDist) # right adj
            elif (course % 360) < (270 - courseErr):
                robot.rotate(rotSpeed, -rotDist) # left adj
        elif correction == "Camera":
            robot.rotate(rotSpeed, rotDist)# right adj
        
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
    if(state == "Straight 1"):
        #Correct heading
        if(isCorrectHeading(distances, cameraObjects, position, course, state)):
            if (isBlue(cameraObjects, "Right")[0]):
                robot.move(moveSpeed , moveDist)
            else:
                correctRobot(robot, distances, cameraObjects, position, course, state, "Camera")
        else:
            correctRobot(robot, distances, cameraObjects, position, course, state, "Heading")

    #Turn 1
    if(state == "Turn 1"):
        robot.rotate(90, 90)







run.algo = algo
#run.isSim = False
run.run()