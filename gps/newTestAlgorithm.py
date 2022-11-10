from enum import Enum
import robot
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

    def algorithm(self, robot):
        self.update_state()

        if self.current_state == State.IDLE:
            robot.stop()
        elif self.current_state == State.DRIVE1 or self.current_state == State.DRIVE2 or self.current_state == State.DRIVE3 or self.current_state == State.DRIVE4 or self.current_state == State.DRIVE5 or self.current_state == State.DRIVE6 or self.current_state == State.DRIVE7:
            robot.drive()
        elif self.current_state == State.TURNRIGHT1 or self.current_state == State.TURNRIGHT2 or self.current_state == State.TURNRIGHT3 or self.current_state == State.TURNRIGHT4:
            robot.turn_right()
        elif self.current_state == State.TURNLEFT1 or self.current_state == State.TURNLEFT2:
            robot.turn_left()        

        #Update variables with sensor data

    def update_state(self):
        match self.current_state:
            case State.IDLE:
                pass
            case State.DRIVE1:
                if self.distance_travelled >= (20 + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT1:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE2:
                if self.distance_travelled >= (self.pythag(10, 30) + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNLEFT1:
                if self.degrees_rotated >= 45:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE3:
                if self.distance_travelled >= (self.pythag(10, 30) + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT2:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE4:
                if self.distance_travelled >= (20 + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNLEFT2:
                if self.degrees_rotated >= 45:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE5:
                if self.distance_travelled >= (20 + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT3:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE6:
                if self.distance_travelled >= (60 + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
            case State.TURNRIGHT4:
                if self.degrees_rotated >= 90:
                    self.degrees_rotated = 0
                    self.current_state += 1
            case State.DRIVE7:
                if self.distance_travelled >= (20 + self.offset_feet) and self.distance_from_obstacle < 1:
                    self.distance_travelled = 0
                    self.current_state += 1
    
    def pythag(a, b):
        return math.sqrt(a*a + b*b)
