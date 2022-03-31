
from cmath import pi


isSim = True

algo = None

pixelsPerMeter = 10 #scaled to keep the size of the robot the same on screen, may need to change later if the course doesn't fit on screen

sensorMaxDistance = 2 #in meters

def run():
    global pixlesPerMeter
    global sensorMaxDistance
    if (algo == None):
        print("Error: Set the algorithm first")
        return
    if (isSim):
        import robot_sim
        FPS = 60
        yellow = (255,255,0,255)
        blue = (0,0,255,255)
        green = (0,255,0,255)
        red = (255,0,0,255)
            # Pixels is the resolution on screen
        # Course resolution is the grid count used to draw a course
        course = robot_sim.Course(pixelsX=100*pixelsPerMeter,
                                pixelsY=100*pixelsPerMeter,
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
        course.circle(x=(midpointX+(30*feetToPixels)), y=(midpointY+(20*feetToPixels)), r=brp, c=blue) #the blue barrels
        course.circle(x=(midpointX+(-30*feetToPixels)), y=(midpointY+(20*feetToPixels)), r=brp, c=blue)
        course.circle(x=(midpointX+(-30*feetToPixels)), y=(midpointY+(-20*feetToPixels)), r=brp, c=blue)
        course.circle(x=(midpointX+(30*feetToPixels)), y=(midpointY+(-20*feetToPixels)), r=brp, c=blue)

        course.circle(x=(midpointX), y=(midpointY+(-10*feetToPixels)), r=brp, c=yellow)

        course.circle(x=(midpointX), y=(midpointY+((20+(gateWidth/2))*feetToPixels)), r=brp, c=red) #top red barrel
        course.circle(x=(midpointX), y=(midpointY+((20-(gateWidth/2))*feetToPixels)), r=brp, c=red) #top red barrel

        course.circle(x=(midpointX+(-31*feetToPixels)), y=(midpointY), r=brp, c=green) #ramp placeholder
        course.circle(x=(midpointX+(31*feetToPixels)), y=(midpointY+(-2*feetToPixels)), r=brp, c=green) #just there for testing purposes

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
            "Left": robot_sim.Sensor(x=0,y=(robot.length-(0.0889*pixelsPerMeter)),d=sensorMaxDistance*pixelsPerMeter,angle=-90,debug=True),
            "FrontLeft": robot_sim.Sensor(x=(0.0254*pixelsPerMeter),y=(0.3302*pixelsPerMeter),d=sensorMaxDistance*pixelsPerMeter,angle=-45,debug=True),
            "Right": robot_sim.Sensor(x=robot.width,y=(robot.length-(0.0889*pixelsPerMeter)),d=sensorMaxDistance*pixelsPerMeter,angle=90,debug=True),
            "FrontRight": robot_sim.Sensor(x=(robot.width-(0.0254*pixelsPerMeter)),y=(0.3302*pixelsPerMeter),d=sensorMaxDistance*pixelsPerMeter,angle=45,debug=True),
            "Front": robot_sim.Sensor(x=4.5,y=robot.length,d=sensorMaxDistance*pixelsPerMeter,angle=0,debug=True)
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
            'main': robot_sim.Camera(x=(robot.length / 2),
                        y=(robot.length / 2),
                        angle=0,
                        fieldOfView=90,
                        splitCount=3, # How many splits are in the camera when showing object colors
                        resolution=40, # How many rays are in the field of view
                        debug=True,
                        maxDistance=300#come back to this
                        )
        }

        cameras['main'].registerColor(green, "Green")
        cameras['main'].registerColor(red, "Red")
        cameras['main'].registerColor(blue, "Blue")
        cameras['main'].registerColor(yellow, "Yellow")

        # Location is pixel placement in display
        # Length and width are in pixels
        robot = robot_sim.RobotSim(location=(700,325),          #
                                length=0.3556 * pixelsPerMeter,
                                width=0.3556 * pixelsPerMeter,
                                algorithm=algo,#Roomba.run,
                                sensors=sensors,
                                cameras=cameras)

        robot_sim.run(course, robot, FPS)
    else:
        from robot import Robot
        r = Robot(algo)

        while (True):
            r.tick()
