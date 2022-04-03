
from cmath import pi


isSim = True

algo = None

debugCamera = False

cameraSplits = 3

error = False

pixelsPerMeter = 40 #scaled to keep the size of the robot the same on screen, may need to change later if the course doesn't fit on screen

sensorMaxDistance = 2 #in meters

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
        bucketRadius = 0.0127   #in meters
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

        # course.circle(x=(midpointX+(-31*feetToPixels)), y=(midpointY), r=brp, c=green) #ramp placeholder
        # course.circle(x=(midpointX+(31*feetToPixels)), y=(midpointY+(-2*feetToPixels)), r=brp, c=green, px=True) #just there for testing purposes

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
            "Left": robot_sim.Sensor(x=0,y=(robotLength-(0.0889*pixelsPerMeter)),d=sensorMaxDistance*pixelsPerMeter,angle=-90,debug=True),
            "FrontLeft": robot_sim.Sensor(x=(0.0254*pixelsPerMeter),y=(0.3302*pixelsPerMeter),d=sensorMaxDistance*pixelsPerMeter,angle=-45,debug=True),
            "Right": robot_sim.Sensor(x=robotWidth,y=(robotLength-(0.0889*pixelsPerMeter)),d=sensorMaxDistance*pixelsPerMeter,angle=90,debug=True),
            "FrontRight": robot_sim.Sensor(x=(robotWidth-(0.0254*pixelsPerMeter)),y=(0.3302*pixelsPerMeter),d=sensorMaxDistance*pixelsPerMeter,angle=45,debug=True),
            "Front": robot_sim.Sensor(x=4.5,y=robotLength,d=sensorMaxDistance*pixelsPerMeter,angle=0,debug=True)
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
                        resolution=140, # How many rays are in the field of view
                        debug=True,
                        maxDistance=25 * feetToPixels #come back to this
                        )
        }

        cameras['main'].registerColor(green, "Green")
        cameras['main'].registerColor(red, "Red")
        cameras['main'].registerColor(blue, "Blue")
        cameras['main'].registerColor(yellow, "Yellow")

        # Location is pixel placement in display
        # Length and width are in pixels
        robot = robot_sim.RobotSim(location=(midpointX + 40*feetToPixels,midpointY),          #
                                length=0.3556 * pixelsPerMeter,
                                width=0.3556 * pixelsPerMeter,
                                algorithm=algo,#Roomba.run,
                                sensors=sensors,
                                cameras=cameras,
                                startingAngle=180,
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
