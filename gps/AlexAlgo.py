import run

# Define some constants and errors(margins) to be used in calculations
distanceErr = .5  # lateral distance error
courseErr = 15.0  # course AKA heading AKA angle error
moveSpeed = 10.0
moveDist = .5
rotSpeed = 270
rotDist = 5
wait_time = .5

# Initial starting state of the Algorithm. Each state is a
# different "cut" or segment of the track the algorithm will focus on.
state = "Straight 1"

# Camera Name to Index dictionary
splitDict = {
    "Left": 0,
    "Front": 1,
    "Right": 2
}


# Color Tests
def isColorPresent(cameraObjects, splitName, color):
    """
    Checks if a color is present in the camera objects and counts how many
    """
    global splitDict

    flag = False
    count = 0
    splitNum = splitDict[splitName]  # get which split index of the camera to use

    # Check every camera object in a split for a color and update the count of them present
    for o in cameraObjects[splitNum]:
        if o["color"] == color:
            flag = True
            count += 1

    return flag, count


def isColorPresentAtAll(cameraObjects, color):
    """
    See isColorPresent. But tests every split instead
    """
    global splitDict

    flag = False
    count = 0

    for splitNum in range(len(splitDict)):
        for o in cameraObjects[splitNum]:
            if o["color"] == color:
                flag = True
                count += 1

    return flag, count


# Heading Tests
def inHeadingRange(course, min, max):
    """
    Is the given course in degrees in range with the min and max with a margin of error.
    """
    global courseErr
    return (min - courseErr) < course < (max + courseErr)


def is_correct_heading(course, state):
    """
    Returns whether the stored heading, depending on state, of the robot matches measured heading by the GPS
    """
    global courseErr
    course_adj = course % 360
    print(course_adj)
    print(inHeadingRange(course_adj, 180, 180))
    if state == "Straight 1":
        # straight to the left towards bottom left blue barrel
        return inHeadingRange(course_adj, 180, 180)
    if state == "Turn 1":
        # from left to almost up
        return inHeadingRange(course_adj, 180, 300)
    if state == "Yellow":
        # general direction of yellow barrel
        return inHeadingRange(course_adj, 180, 340)
    if state == "Straight 2":
        # general direction of top left blue barrel
        return inHeadingRange(course_adj, 180, 270)
    if state == "Turn 2":
        # from left to right clockwise. "0" is added here so error can be included once crossing 0(facing right).
        return inHeadingRange(course_adj, 180, 360) or inHeadingRange(course_adj, 0, 0)
    if state == "Straight 3":
        # straight right with inclusion of both "0"'s
        return inHeadingRange(course_adj, 360, 360) or inHeadingRange(course_adj, 0, 0)
    if state == "Turn 3":
        # from right to down
        return inHeadingRange(course_adj, 360, 360) or inHeadingRange(course_adj, 0, 90)
    if state == "Tunnel":
        # 85 deg. from testing toward red tunnel
        return inHeadingRange(course_adj, 85, 85)
    if state == "Straight 4":
        # straight to the left
        return inHeadingRange(course_adj, 70, 90)
    if state == "Turn 4":
        # down to left
        return inHeadingRange(course_adj, 90, 180)
    if state == "Straight 5":
        # straight to the left to finish
        return inHeadingRange(course_adj, 180, 180)


# State Tests
def update_state(cameraObjects, course, state):
    """
    Changes the state of the algorithm depending on the sensor inputs.
    Changes can come from color detection, heading change, etc.
    """
    # Edge case, ignore.
    if state == None:
        print("state was None")
        state = "Straight 1"

    if state == "Straight 1":
        # Once we pass the barrel, camera can't see it, we should start turning
        if not isColorPresent(cameraObjects, "Front", "Blue")[0] and course < (315 + courseErr):
            return "Turn 1"
        else:
            return state

    if state == "Turn 1":
        # Turn until we see the yellow or we've turned too much
        # print(course)
        if isColorPresent(cameraObjects, "Front", "Yellow")[0] or course > (300 + courseErr):
            return "Find Yellow"
        else:
            return state

    if state == "Find Yellow":
        # check for when we see the yellow barrel and can navigate around it
        print("Searching for Yellow")
        if isColorPresent(cameraObjects, "Left", "Yellow")[0]:
            return "Yellow"
        else:
            return state

    if state == "Yellow":
        # Wait until we turn enough to start heading for blue
        if not (course % 360) > 255 - courseErr:
            return "Find Blue 1"
        else:
            return state

    if state == "Find Blue 1":
        # check for when we see the blue barrel and can navigate around it
        print("Searching for Blue 1")
        if isColorPresentAtAll(cameraObjects, "Blue")[0]:
            return "Straight 2"
        else:
            return state

    if state == "Straight 2":
        # Go straight until we see the next blue barrel
        if not isColorPresentAtAll(cameraObjects, "Blue")[0] and (course % 360) < (235 + courseErr):
            return "Turn 2"
        else:
            return state

    if state == "Turn 2":
        # Turn until we've turned too much(values tested)
        # print(course % 360)
        if (course % 360) > 10 - courseErr and (course % 360) < 20 + courseErr:
            return "Find Blue 2"
        else:
            return state

    if state == "Find Blue 2":
        # print("Searching for Blue 2")
        if isColorPresent(cameraObjects, "Right", "Blue")[0]:
            return "Straight 3"
        else:
            return state

    if state == "Straight 3":
        if not isColorPresentAtAll(cameraObjects, "Blue")[0] and (
                (course % 360) > 360 - courseErr or (course % 360) < (0 + courseErr)):
            return "Turn 3"
        else:
            return state

    if state == "Turn 3":
        # print(course % 360)
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
        # Drive until we can see the tunnel and should move onto barrels again
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
        if not isColorPresentAtAll(cameraObjects, "Blue")[0] and (
                (course % 360) > 70 - courseErr or (course % 360) < (90 + courseErr)):
            return "Turn 4"
        else:
            return state

    if state == "Turn 4":
        # print(course % 360)
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
        print("WWCD")
        return "Finish"


# Movement Correction
def correctRobot(robot, cameraObjects, course, state, correction):
    """
    Determine how to adjust the robot with a correction type and state.
    Heading adjustments are due to the robot sway off to one direction
    Camera adjustments are when the camera cannot see anything and must rotate the appropriate way
    """
    global rotSpeed
    global rotDist

    if state == "Straight 1":
        print(10)
        if correction == "Heading":
            if (course % 360) > (180 + courseErr):
                robot.rotate(rotSpeed, rotDist)  # right adj
            elif (course % 360) < (180 - courseErr):
                robot.rotate(-rotSpeed, rotDist)  # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Turn 1":
        if correction == "Heading":
            if (course % 360) > (0 + courseErr):
                robot.rotate(rotSpeed, rotDist)  # right adj
            elif (course % 360) < (180 - courseErr):
                robot.rotate(-rotSpeed, rotDist)  # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Yellow":
        if correction == "Camera":
            robot.constantRotate(-rotSpeed)

    if state == "Straight 2":
        if correction == "Heading":
            if (course % 360) > (270 + courseErr):
                robot.rotate(rotSpeed, rotDist)  # right adj
            elif (course % 360) < (180 - courseErr):
                robot.rotate(-rotSpeed, rotDist)  # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Turn 2":
        if correction == "Heading":
            if (course % 360) > (0 + courseErr) and (course % 360) < (90):
                robot.rotate(-rotSpeed, rotDist)  # left adj
            elif (course % 360) < (180 - courseErr) and (course % 360) > (90):
                robot.rotate(rotSpeed, rotDist)  # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Straight 3":
        if correction == "Heading":
            if (course % 360) < (360 - courseErr) and (course % 360) > 180:
                robot.rotate(rotSpeed, rotDist)  # right adj
            elif (course % 360) > (0 + courseErr) and (course % 360) < 180:
                robot.rotate(-rotSpeed, rotDist)  # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Turn 3":
        if correction == "Heading":
            if (course % 360) > (0 + courseErr) and (course % 360) < (90):
                robot.rotate(-rotSpeed, rotDist)  # left adj
            elif (course % 360) < (180 - courseErr) and (course % 360) > (90):
                robot.rotate(rotSpeed, rotDist)  # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Tunnel":
        if correction == "Heading":
            print("heading adj")
            if (course % 360) > (85 + courseErr):
                robot.rotate(-rotSpeed, rotDist)  # left adj
            elif (course % 360) < (85 - courseErr):
                robot.rotate(rotSpeed, rotDist)  # right adj
        elif correction == "Camera":
            # more complicated camera calculation. tries to avoid the walls using both left and right camera splits.
            print("camera adj")
            if isColorPresent(cameraObjects, "Left", "Red")[1] > 1:
                robot.rotate(-rotSpeed, rotDist)  # left adj
            if isColorPresent(cameraObjects, "Right", "Red")[1] > 1:
                robot.rotate(rotSpeed, rotDist)  # right adj
            if isColorPresent(cameraObjects, "Left", "Red")[1] == 1 and not \
                    isColorPresent(cameraObjects, "Right", "Red")[1] == 1:
                robot.constantMove(moveSpeed)
            if isColorPresent(cameraObjects, "Right", "Red")[1] == 1 and not \
                    isColorPresent(cameraObjects, "Left", "Red")[1] == 1:
                robot.constantMove(moveSpeed)

    if state == "Straight 4":
        if correction == "Heading":
            if (course % 360) > (90 + courseErr):
                robot.rotate(-rotSpeed, rotDist)  # left adj
            elif (course % 360) < (90 - courseErr):
                robot.rotate(rotSpeed, rotDist)  # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Turn 4":
        if correction == "Heading":
            if (course % 360) > (180 + courseErr):
                robot.rotate(-rotSpeed, rotDist)  # left adj
            elif (course % 360) < (90 - courseErr):
                robot.rotate(rotSpeed, rotDist)  # right adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj

    if state == "Straight 5":
        if correction == "Heading":
            if (course % 360) < (360 - courseErr) and (course % 360) > 180:
                robot.rotate(rotSpeed, rotDist)  # right adj
            elif (course % 360) > (0 + courseErr) and (course % 360) < 180:
                robot.rotate(-rotSpeed, rotDist)  # left adj
        elif correction == "Camera":
            robot.constantRotate(rotSpeed)  # right adj


# Algorithm
def algo(robot, t, events=None):
    """
    Tick of the algorithm. Takes in the robot and starts in the state "Straight 1".
    Depending on the state it will determine how to move(forward, left, right, stop, etc.)
    REQUIREMENTS FOR ALGORITHM: distance sensors, GPS, camera
    """
    global state

    global wait_time
    distances = robot.getSensorData()
    cameraObjects = robot.getCameraData()["main"]
    position = robot.getPosition()
    course = robot.getAngle()

    # print(cameraObjects)
    print(state)

    # Crash Prevention <3
    if distances["Front"] < .5:
        robot.stop()

    # Update state after new data and after we have gotten close enough to the first blue barrel
    if t >= wait_time:
        course_adj = course % 360
        state = update_state(cameraObjects, course_adj, state)
        if state == "Finish":
            robot.stop()
            return 
    else:
        state = "Straight 1"
    # Straight 1
    if (state == "Straight 1"):
        # Correct heading
        # wait so robot can reach first barrel
        if t < wait_time:
            robot.constantMove(moveSpeed)
            return
        if (is_correct_heading(course, state)):
            if (isColorPresent(cameraObjects, "Front", "Blue")[0]):
                robot.constantRotate(-rotSpeed)  # left adj
            # elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            #     robot.constantMove(moveSpeed)
            # else:
            #     print("camera adj")
            #     correctRobot(robot, cameraObjects, course, state, "Camera")
            else:
                robot.constantMove(moveSpeed)
        else:
            print("heading adj")
            correctRobot(robot, cameraObjects, course, state, "Heading")

    # Turn 1
    if (state == "Turn 1"):
        if (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            robot.constantMove(moveSpeed)
        else:
            print("camera adj")
            correctRobot(robot, cameraObjects, course, state, "Camera")

    if state == "Find Yellow":
        robot.constantMove(moveSpeed)

    # Yellow
    if state == "Yellow":
        if (is_correct_heading(course, state)):

            if (isColorPresent(cameraObjects, "Right", "Yellow")[0] or
                    isColorPresent(cameraObjects, "Front", "Yellow")[0]):
                robot.constantRotate(rotSpeed)  # right adj
            elif (isColorPresent(cameraObjects, "Left", "Yellow")[0]):
                robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, cameraObjects, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, cameraObjects, course, state, "Heading")

    if state == "Find Blue 1":
        robot.constantMove(moveSpeed)

    if state == "Straight 2":
        print("Straight 2")
        # Correct heading
        if is_correct_heading(course, state):
            if isColorPresent(cameraObjects, "Front", "Blue")[0]:
                robot.constantRotate(-rotSpeed)  # left adj
            elif isColorPresent(cameraObjects, "Right", "Blue")[0]:
                robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, cameraObjects, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, cameraObjects, course, state, "Heading")

    # Turn 2
    if (state == "Turn 2"):
        if isColorPresent(cameraObjects, "Right", "Blue")[0]:
            robot.constantMove(moveSpeed)
        else:
            print("camera adj")
            correctRobot(robot, cameraObjects, course, state, "Camera")

    if state == "Find Blue 2":
        robot.constantMove(moveSpeed)

    if state == "Straight 3":
        print("Straight 3")
        # Correct heading
        if (is_correct_heading(course, state)):
            if (isColorPresent(cameraObjects, "Front", "Blue")[0]):
                robot.constantRotate(-rotSpeed)  # left adj
            elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
                robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, cameraObjects, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, cameraObjects, course, state, "Heading")

    # Turn 2
    if (state == "Turn 3"):
        if (isColorPresent(cameraObjects, "Right", "Blue")[0]):
            robot.constantMove(moveSpeed)
        else:
            print("camera adj")
            correctRobot(robot, cameraObjects, course, state, "Camera")

    if state == "Find Red":
        robot.constantMove(moveSpeed)

    if state == "Tunnel":
        if is_correct_heading(course, state):
            if isColorPresentAtAll(cameraObjects, "Red"):
                robot.constantMove(moveSpeed)
            elif (isColorPresent(cameraObjects, "Left", "Red")[1] == 1 and
                  isColorPresent(cameraObjects, "Right", "Red")[1] == 1):
                robot.constantMove(moveSpeed)
            elif (isColorPresent(cameraObjects, "Front", "Red")[1] == 2):
                robot.constantMove(moveSpeed)
            else:
                correctRobot(robot, cameraObjects, course, state, "Camera")
        else:
            correctRobot(robot, cameraObjects, course, state, "Heading")

    if state == "Find Blue 3":
        if isColorPresent(cameraObjects, "Front", "Blue")[0] or isColorPresent(cameraObjects, "Left", "Blue")[0]:
            robot.constantRotate(-rotSpeed)
        else:
            robot.constantMove(moveSpeed)

    if state == "Straight 4":
        print("Straight 4")
        # Correct heading
        if (is_correct_heading(course, state)):
            if (isColorPresent(cameraObjects, "Front", "Blue")[0]):
                robot.constantMove(moveSpeed)
            elif (isColorPresent(cameraObjects, "Left", "Blue")[0]):
                robot.constantRotate(-rotSpeed)  # left adj
            elif (isColorPresent(cameraObjects, "Right", "Blue")[0]):
                robot.constantMove(moveSpeed)
            else:
                print("camera adj")
                correctRobot(robot, cameraObjects, course, state, "Camera")
        else:
            print("heading adj")
            correctRobot(robot, cameraObjects, course, state, "Heading")

    # Turn 2
    if (state == "Turn 4"):
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
            correctRobot(robot, cameraObjects, course, state, "Camera")

    if state == "Straight 5":
        robot.constantMove(moveSpeed)


run.algo = algo
# run.isSim = False
run.run()
