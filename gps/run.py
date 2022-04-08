
from cmath import pi
import math
import random

isSim = True

algo = None

debugCamera = False

cameraSplits = 3

error = False

pixelsPerMeter = 40

sensorMaxDistance = 2

scenario = "MAIN"

startingOffsetError = (0,0)

positionError=0
angleError=0
moveError=0
rotationError=0
sensorError=0

if (error):
    positionError=3
    angleError=5
    moveError=15
    rotationError=15
    sensorError=0.04



def run():
    global pixlesPerMeter
    global sensorMaxDistance
    if (algo == None):
        print("Error: Set the algorithm first")
        return
    if (isSim):
        robotLength = 0.3556 * pixelsPerMeter
        robotWidth = 0.3556 * pixelsPerMeter
        import robot_sim
        FPS = 60
        yellow = (255,255,0,255)
        blue = (0,0,255,255)
        green = (0,255,0,255)
        red = (255,0,0,255)
        # Pixels is the resolution on screen
        # Course resolution is the grid count used to draw a course
        course = robot_sim.Course(pixelsX=25*pixelsPerMeter,
                                pixelsY=25*pixelsPerMeter,
                                courseResolutionX=220,          
                                courseResolutionY=220,          
                                pixelsPerMeter=pixelsPerMeter)


        # -- Draw course --
        #defining some useful constants
        bucketRadius = 0.07   #in meters
        brp = bucketRadius*pixelsPerMeter       #(b)ucket (r)adius in (p)ixels
        midpointX = (course.pixelsX)/2
        midpointY = (course.pixelsY)/2
        feetToMeters = .3048
        feetToPixels = feetToMeters*pixelsPerMeter
        gateWidth = 5 #in feet
        #course.createOuterWalls(c=white)

        #these next lines make the barrels the numbers are in feet (NOT meters)
        x=(midpointX+(30*feetToPixels))
        y=(midpointY-(20*feetToPixels))
        print(x,y)
        course.circle(x,y, r=brp, c=blue, px=True) #the blue barrels
        course.circle(x=(midpointX+(-30*feetToPixels)), y=(midpointY-(20*feetToPixels)), r=brp, c=blue, px=True)
        course.circle(x=(midpointX+(-30*feetToPixels)), y=(midpointY-(-20*feetToPixels)), r=brp, c=blue, px=True)
        course.circle(x=(midpointX+(30*feetToPixels)), y=(midpointY-(-20*feetToPixels)), r=brp, c=blue, px=True)
        course.circle(x=(midpointX), y=(midpointY-(-10*feetToPixels)), r=brp, c=yellow, px=True)
        course.circle(x=(midpointX), y=(midpointY-((20+(gateWidth/2))*feetToPixels)), r=brp, c=red, px=True) #top red barrel
        course.circle(x=(midpointX), y=(midpointY-((20-(gateWidth/2))*feetToPixels)), r=brp, c=red, px=True) #top red barrel


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
            "Left": robot_sim.Sensor(x=0,y=(robotLength-(0.0889*pixelsPerMeter)),d=sensorMaxDistance*pixelsPerMeter,angle=-90,debug=True,coneAngle=5),
            "FrontLeft": robot_sim.Sensor(x=(0.0254*pixelsPerMeter),y=(0.3302*pixelsPerMeter),d=sensorMaxDistance*pixelsPerMeter,angle=-45,debug=True,coneAngle=5),
            "Right": robot_sim.Sensor(x=robotWidth,y=(robotLength-(0.0889*pixelsPerMeter)),d=sensorMaxDistance*pixelsPerMeter,angle=90,debug=True,coneAngle=5),
            "FrontRight": robot_sim.Sensor(x=(robotWidth-(0.0254*pixelsPerMeter)),y=(0.3302*pixelsPerMeter),d=sensorMaxDistance*pixelsPerMeter,angle=45,debug=True,coneAngle=5),
            "Front": robot_sim.Sensor(x=robotWidth/2,y=robotLength,d=sensorMaxDistance*pixelsPerMeter,angle=0,debug=True,coneAngle=10),
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
            'main': robot_sim.Camera(x=(robotLength / 2),
                        y=(robotLength / 2),
                        angle=0,
                        fieldOfView=160,
                        splitCount=cameraSplits, # How many splits are in the camera when showing object colors
                        resolution=400, # How many rays are in the field of view
                        debug=True,
                        maxDistance=15*feetToPixels #come back to this
                        )
        }

        cameras['main'].registerColor(green, "Green")
        cameras['main'].registerColor(red, "Red")
        cameras['main'].registerColor(blue, "Blue")
        cameras['main'].registerColor(yellow, "Yellow")

        # Location is pixel placement in display
        # Length and width are in pixels
        angle = 0
        if (scenario == "MAIN"):
            angle = 180
            sx = midpointX + 25*feetToPixels + random.uniform(-startingOffsetError[0], startingOffsetError[0])*pixelsPerMeter
            sy = midpointY + random.uniform(-startingOffsetError[1], startingOffsetError[1])*pixelsPerMeter
        if (scenario == "RED"):
            angle = 90
            sx = 20*feetToPixels + random.uniform(-startingOffsetError[0], startingOffsetError[0])*pixelsPerMeter
            sy = 20*feetToPixels + random.uniform(-startingOffsetError[1], startingOffsetError[1])*pixelsPerMeter
        robot = robot_sim.RobotSim(location=(sx,sy),          #
                                length=0.3556 * pixelsPerMeter,
                                width=0.3556 * pixelsPerMeter,
                                algorithm=algo,#Roomba.run,
                                sensors=sensors,
                                cameras=cameras,
                                startingAngle=angle,
                                angleError=angleError,
                                positionError=positionError,
                                moveError=moveError,
                                rotationError=rotationError,
                                sensorError=sensorError)

        robot_sim.run(course, robot, FPS)
    else:
        from robot import Robot
        from camera import Camera
        r = Robot(algo, Camera(cameraSplits, debugCamera, "main"))

        while (True):
            r.tick()
