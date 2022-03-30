
isSim = True

algo = None

def run():
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

        cameras['main'].registerColor(green, "Green")
        cameras['main'].registerColor(red, "Red")
        cameras['main'].registerColor(blue, "Blue")
        cameras['main'].registerColor(yellow, "Yellow")

        # Location is pixel placement in display
        # Length and width are in pixels
        robot = robot_sim.RobotSim(location=(700,325),          #
                                length=19,
                                width=9,
                                algorithm=algo,#Roomba.run,
                                sensors=sensors,
                                cameras=cameras)

        robot_sim.run(course, robot, FPS)
    else:
        from robot import Robot
        r = Robot(algo)

        while (True):
            r.tick()
