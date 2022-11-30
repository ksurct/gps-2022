from enum import Enum
import math

class State(Enum):
    DRIVE1 = 0
    TURNRIGHT1 = 1
    DRIVE2 = 2
    TURNLEFT1 = 3
    DRIVE3 = 4
    TURNRIGHT2 = 5
    DRIVE4 = 6
    TURNLEFT2 = 7 # Avoid ramp
    DRIVE5 = 8
    TURNRIGHT3 = 9
    DRIVE6 = 10
    TURNRIGHT4 = 11
    DRIVE7 = 12
    IDLE = 13

class newTestAlgorithm:
    def __init__(self):
        self.distance_travelled = 0
        self.degrees_rotated = 0
        self.distance_from_obstacle = 0
        self.current_state = State.IDLE
        self.offset_feet = 2
        def dsen():
            return {"Front": -1, "FrontRight": -1, "FrontLeft": -1, "Left": -1, "Right": -1}
        self.sensorList = [dsen(), dsen(), dsen()]
        self.callSensorListOnce = True
        self.sensorData = None

    def algorithm(self, robot):
        self.update_sensors()

        self.update_state()

        if self.current_state == State.IDLE:
            robot.stop()
        elif self.current_state == State.DRIVE1 or self.current_state == State.DRIVE2 or self.current_state == State.DRIVE3 or self.current_state == State.DRIVE4 or self.current_state == State.DRIVE5 or self.current_state == State.DRIVE6 or self.current_state == State.DRIVE7:
            robot.drive()
        elif self.current_state == State.TURNRIGHT1 or self.current_state == State.TURNRIGHT2 or self.current_state == State.TURNRIGHT3 or self.current_state == State.TURNRIGHT4:
            robot.turn_right()
        elif self.current_state == State.TURNLEFT1 or self.current_state == State.TURNLEFT2:
            robot.turn_left()        

    def update_state(self):
        match self.current_state:
            case State.IDLE:
                pass
            case State.DRIVE1:
                if self.distance_travelled >= (20 + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT1:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE2:
                if self.distance_travelled >= (self.pythag(10, 30) + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNLEFT1:
                if self.degrees_rotated >= 45:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE3:
                if self.distance_travelled >= (self.pythag(10, 30) + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT2:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE4:
                if self.distance_travelled >= (20 + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNLEFT2:
                if self.degrees_rotated >= 45:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE5:
                if self.distance_travelled >= (20 + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT3:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE6:
                if self.distance_travelled >= (60 + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT4:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE7:
                if self.distance_travelled >= (20 + self.offset_feet) or self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
    
    def pythag(a, b):
        return math.sqrt(a*a + b*b)

    def update_sensors(self, robot):
        print("called")
        self.sensorData = robot.getSensorData()

    def get_sensor_list(self, robot):
        if (self.callSensorListOnce):
            data = robot.getSensorData()
            self.sensorList.insert(0, data)
            self.sensorList.pop(len(self.sensorList) - 1)
            self.callSensorListOnce = False
        return self.sensorList
