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
Kd = 0.001

right = 0
left = 0

lastError = 0
position = 60
desiredposition = 0
percentpeed = 20
Loopcount = 0

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
    global percentspeed
    global error
    global Loopcount
    global right
    global left

    error = desiredposition - position

    P = error
    I = I + error
    D = error - lastError
    lastError = error
    

    percentspeed = P*Kp + I*Ki + D*Kd

    right = (100 - percentspeed)
    left = (percentspeed)

    if(right > left):
        position = position + (percentspeed)
    elif(left > right):
        position = position - (percentspeed)


    #if (percentspeed > 0.5):
         

Flag = True

while True:
    
    # if (position > 360):
    #     position = 0
    
    # if (position < 0):
    #     position = 360
    
    PID_control()
    print("percentspeed: ", percentspeed)
    print("Position: ", position)

    print("Right: ", right)
    print("Left: ", left)
    print("Error: ", error)
    print("Loopcount: ", Loopcount)
    input()
    Loopcount = Loopcount + 1









