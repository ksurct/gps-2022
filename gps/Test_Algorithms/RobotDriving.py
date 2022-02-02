import robot_sim
import random
import pygame

# Target FPS
FPS = 60
flip = False
white = (255,255,255,255)
blue = (0,0,255,255)
green = (0,255,0,255)
red = (255,0,0,255)
yellow = (255, 255 , 0, 255)
mod = 0
flag = 0
is_blue = False


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
    # 'events' from pygame
    # 'time' time since start of program in seconds
    sensorData = robot.getSensorData()
    cameraData = robot.getCameraData()
    keyboard(events)
    # in degrees
    angle = robot.getAngle()
    # Probable x,y coordinates
    position = robot.getPosition()
    print("------------------")
    #for sensorName in sensorData:
        #print(sensorName, 'distance =', sensorData[sensorName])

    for cameraName in cameraData.keys():
        camera = cameraData[cameraName]
        # Do something
        
        for split in camera:
            
            #print("[", end="")
            for object in split:
                '''
                if (object == blue):
                    print("blue,", end="")
                elif (object == white):
                    print("white,", end="")
                elif (object == green):
                    print("green,", end="")
                elif (object == red):
                    print("red,", end="")
                '''

            #print("]")
            print(split)

        if blue in camera[2] or blue in camera[1]:
            robot.rotate(30,10)
        elif blue in camera[0]:
            is_blue = True
            robot.move(30,30)
        elif is_blue:
            robot.rotate(-30,10)
        else:
            robot.move(30,30)

            


        
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


# Pixels is the resolution on screen
# Course resolution is the grid count used to draw a course
course = robot_sim.Course(pixelsX=1000,
                          pixelsY=800,
                          courseResolutionX=220,
                          courseResolutionY=180)


# -- Draw course --
course.createOuterWalls(c=white)

course.circle(x=40, y=30, r=2, c=blue)
course.circle(x=40,y=140,r=2,c=blue)
course.circle(x=170,y=30,r=2,c=blue)
course.circle(x=170,y=140,r=2,c=blue)

course.circle(x =107,y=120,r=2,c=yellow)

# course.circle(x = 90, y=120, r=2, c=yellow)





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
    "TL": robot_sim.Sensor(x=0,y=50,d=300,angle=-90,debug=False),
    "BL": robot_sim.Sensor(x=0,y=0,d=300,angle=-90,debug=False),
    "BR": robot_sim.Sensor(x=25,y=0,d=300,angle=90,debug=False),
    "TR": robot_sim.Sensor(x=25,y=50,d=300,angle=90,debug=False),
    "Front": robot_sim.Sensor(x=4.5,y=9.5,d=300,angle=0,debug=True)
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
                   debug=True
                   )
}

# Location is pixel placement in display
# Length and width are in pixels
robot = robot_sim.RobotSim(location=(850,400),
                           length=19,
                           width=9,
                           algorithm=algorithm,
                           sensors=sensors,
                           cameras=cameras)

robot_sim.run(course, robot, FPS)
