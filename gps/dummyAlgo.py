


SIM = False

flip = False
white = (255,255,255,255)
blue = (0,0,255,255)
green = (0,255,0,255)
red = (255,0,0,255)
mod = 0
if (not SIM):
    white = "White"
    red = "Red"
    green = "Green"
    blue = "Blue"

# Algorithm
# Called every 'tick' 1/FPS
# This is a dummy algorithm that shows how to a control a robot
def algorithm(robot, time, events = None):
    global white
    global blue
    global flip
    global green
    global red
    global mod
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
                if (object['color'] == blue):
                    print("(blue,{}),".format(object['size']), end="")
                elif (object['color'] == white):
                    print("(white,{}),".format(object['size']), end="")
                elif (object['color'] == green):
                    print("(green,{}),".format(object['size']), end="")
                elif (object['color'] == red):
                    print("(red,{}),".format(object['size']), end="")
            print("]")

    if (sensorData['Front'] < 100 and sensorData['Front'] != -1):
        while (mod == 0):
            mod = random.randrange(-1,2)
        robot.rotate(2 * mod, 35)
    elif (robot.isNotMoving()):
        mod = 0
        robot.constantMove(2)








if (SIM):
    import robot_sim
    import random
    import pygame

    # Target FPS
    FPS = 60

    # Pixels is the resolution on screen
    # Course resolution is the grid count used to draw a course
    course = robot_sim.Course(pixelsX=800,
                            pixelsY=800,
                            courseResolutionX=180,
                            courseResolutionY=180)


    # -- Draw course --
    course.createOuterWalls(c=white)

    course.circle(x=100,y=100,r=20,c=blue)
    course.circle(x=50,y=180,r=10,c=red)
    course.circle(x=75,y=25,r=5,c=green)

    course.box(x1=150,y1=10,x2=160,y2=180,c=green)
    course.box(x1=30,y1=150,x2=40,y2=40,c=red)



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
        "TL": robot_sim.Sensor(x=0,y=50,d=300,angle=-90,debug=False),
        "BL": robot_sim.Sensor(x=0,y=0,d=300,angle=-90,debug=False),
        "BR": robot_sim.Sensor(x=25,y=0,d=300,angle=90,debug=False),
        "TR": robot_sim.Sensor(x=25,y=50,d=300,angle=90,debug=False),
        "Front": robot_sim.Sensor(x=12.5,y=50,d=300,angle=0,debug=True)
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
        'main': robot_sim.Camera(x=12.5,
                    y=25,
                    angle=0,
                    fieldOfView=170,
                    splitCount=3, # How many splits are in the camera when showing object colors
                    resolution=40, # How many rays are in the field of view
                    debug=True,
                    maxDistance=300
                    )
    }

    # Location is pixel placement in display
    # Length and width are in pixels
    robot = robot_sim.RobotSim(location=(100,100),
                            length=50,
                            width=25,
                            algorithm=algorithm,
                            sensors=sensors,
                            cameras=cameras)

    robot_sim.run(course, robot, FPS)

else:

    from robot import Robot
    r = Robot(algorithm)

    while (True):
        r.tick()
