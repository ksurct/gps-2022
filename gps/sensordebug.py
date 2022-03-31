import run

def sensorDebugAlgo(robot, t, events=None):

    print(robot.getSensorData())


run.algo = sensorDebugAlgo
#run.isSim=False
run.run()