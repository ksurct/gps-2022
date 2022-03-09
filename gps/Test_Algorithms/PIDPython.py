# from simple_pid import PID
# pid = PID(1, 0.1, 0.05, setpoint=1)

# # Assume we have a system we want to control in controlled_system
# v = controlled_system.update(0)

# while True:
#     # Compute new output from the PID according to the systems current value
#     control = pid(v)

#     # Feed the PID output to the system and get its current value
#     v = controlled_system.update(control)


# from simple_pid import PID


# currentangle = 0

# PID.sample_time = 0.01 #Update ever 0.01 seconds

# while True:
#     output = PID(currentangle)

P = 0
I = 0
D = 0

Kp = 0.1
Ki = 0.1
Kd = 0.1

lastError = 0
position = 40
desiredposition = 360
motorspeed = 0

error = 0

def PID_control():
    
    global P
    global I
    global D
    global Kp
    global Ki
    global Kd
    global lastError
    global position 
    global desiredposition
    global motorspeed
    global error

    error = desiredposition - position

    P = error
    I = I + error
    D = error - lastError
    lastError = error
    

    motorspeed = P*Kp + I*Ki + D*Kd

    position = position + motorspeed

Flag = True

while True:
    
    # if (position > 360):
    #     position = 0
    
    # if (position < 0):
    #     position = 360
    
    PID_control()
    print("Motorspeed: ", motorspeed)
    print("Position: ", position)
    print("Error: ", error)
    input()









