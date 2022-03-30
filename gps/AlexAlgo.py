from turtle import distance, position
import run

def algo(robot, t, events=None):

    distances = robot.getSensorData()
    camera = robot.getCameraData()["main"]
    position = robot.getPosition()
    course = robot.getAngle()


    





run.algo = algo
#run.isSim = False
run.run()