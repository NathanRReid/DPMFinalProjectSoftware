from utils.brick import BP, Motor, reset_brick
import sensors
import time, math



# Initialize motors with reverse orientation
left_wheel = Motor("A")
right_wheel = Motor("B")
arm_motor = Motor("C")

'''
# Constants for motor power levels and walking intervals
WHEEL_SPEED = -30  # Reversed for wheel orientation
ARM_POSITION = -30  # Reversed for arm positioning
#arm_motor.set_limits(power=30)  # Lower power
RW = 0.021
RB = 0.053
DISTTODEG = 180 / (math.pi * RW)
ORIENTTODEG = RB / RW
'''

left_wheel.reset_encoder()
right_wheel.reset_encoder()
arm_motor.reset_encoder()

'''
#moves approx 1 unit per dist, stops early and returns true if ultra < 10 or floor is blue.
def MoveDistForward(dist):
    dist = dist * -0.15
    #print(int(dist * DISTTODEG))
    left_wheel.set_limits(power=50)
    right_wheel.set_limits(power=50)
    left_wheel.set_position_relative(int(dist * DISTTODEG))
    right_wheel.set_position_relative(int(dist * DISTTODEG))

    i = -dist * 6
    while (i > 0):
        flag = ultra.get_value() < 10
        if flag:
            left_wheel.set_power(0)
            right_wheel.set_power(0)
            return "wall"
        cval = getFloorColor()
        #print(cval)
        flag = flag or cval == "blue" or cval == "yellow"
        if flag:
            left_wheel.set_power(0)
            right_wheel.set_power(0)
            return "floor"
        STEP = 0.05
        i = i - STEP
        time.sleep(STEP)
    return "done"
'''

def charge():
    left_wheel.set_power(-50)
    right_wheel.set_power(-50)
    time_left = 5#only try for max five seconds
    flag = False
    while (time_left > 0):
        dist = float(sensors.getFrontDistance())
        if (sensors.getFloorColor() == "blue"):
            print("blue in way!")
            flag = True
            break
        if (dist < 10):
            print("early stop!")
            break
        time_left = time_left - 0.05
        time.sleep(0.05)
        
    if not flag:
        left_wheel.set_power(-20)
        right_wheel.set_power(-20)
        time.sleep(0.5)
        
        left_wheel.set_power(0)
        right_wheel.set_power(0)
        left_wheel.reset_encoder()
        right_wheel.reset_encoder()
        detect_and_grab()
        
        #undo slow move forwards
        left_wheel.set_power(20)
        right_wheel.set_power(20)
        time.sleep(0.5)
    
    #return function here
    left_wheel.set_power(50)
    right_wheel.set_power(50)
    while (time_left < 5):
        time_left = time_left + 0.05
        time.sleep(0.05)

def detect_and_grab():
    col = sensors.getFrontColor()
    if (col != "orange" and col != "yellow"):
        print(col, "ABORT NOPE ABORT NOPE")
        return
    DRIVE = 0.7
    arm_motor.set_limits(40)
    arm_motor.set_position(-60)
    time.sleep(1)
    left_wheel.set_power(-50)
    right_wheel.set_power(-50)
    time.sleep(DRIVE)
    left_wheel.set_power(0)
    right_wheel.set_power(0)
    arm_motor.set_position(0)
    time.sleep(1)
    
    left_wheel.set_power(-20)
    right_wheel.set_power(-20)
    time.sleep(0.5)#drive forwards a bit to get it stuck inside
    
    left_wheel.set_power(50)
    right_wheel.set_power(50)
    time.sleep(DRIVE)
    left_wheel.set_power(0)
    right_wheel.set_power(0)


def wall_follow():
    while (True):
        stopped = sub_follow_wall()
        if (stopped == "wall"):
            if False and sensors.getFloorColor() == "yellow":
                left_wheel.set_power(-30)
                right_wheel.set_power(-30)
                time.sleep(2)
                left_wheel.set_power(0)
                right_wheel.set_power(0)
                return
            TURN = 0.5
            left_wheel.set_power(30)
            right_wheel.set_power(-30)
            time.sleep(TURN)
            left_wheel.set_power(-30)
            time.sleep(0.8)
            left_wheel.set_power(30)
            time.sleep(TURN)
            
def sub_follow_wall():
    left_wheel.set_power(-50)
    right_wheel.set_power(-50)
    time_left = 5#only try for max two seconds
    flag = False
    
    while (time_left > 0):
        
        floor_color = sensors.getFloorColor()
        #stop at blue or yellow (UNWRITTEN: END OF PROGRAM, DEPOSIT CUBES
        if (floor_color == "blue" or floor_color == "yellow"):
            print(floor_color, " in way!")
            flag = True
            break
        
        dist = float(sensors.getFrontDistance())
        #US detected wall or cube, if cube collect, if wall turn.
        if (dist < 10):
            print("early stop! Checking for if wall or cube")
            left_wheel.set_power(0)
            right_wheel.set_power(0)
            arm_motor.set_limits(40)
            arm_motor.set_position(-60)
            time.sleep(1)
            new_dist = float(sensors.getFrontDistance())
            print(new_dist)
            arm_motor.set_position(0)
            time.sleep(1)
            if(new_dist < 10): # then it is a wall
                return "wall"
            break
        
        diag = sensors.getDiag()
        #diag US detected something, attempt collection of cube to left.
        if (diag < 20):
            retrieveDiagCube()
        
        time_left = time_left - 0.05
        time.sleep(0.05)
        
    if (flag):
        left_wheel.set_power(0)
        right_wheel.set_power(0)
        #return function, ONLY EXECUTES ON BLUE AND YELLOW, the latter of which is the only color adj to walls
        return
    
    left_wheel.set_power(-20)
    right_wheel.set_power(-20)
    time.sleep(0.5)
    
    left_wheel.set_power(0)
    right_wheel.set_power(0)
    left_wheel.reset_encoder()
    right_wheel.reset_encoder()
    detect_and_grab()
    return "elapsed"
    #return function here

#rotates to face where diag US points, then charge(), then unrotate back to where you where
def retrieveDiagCube():
    print("retrieve!")
    left_wheel.set_power(0)
    right_wheel.set_power(0)
    time.sleep(10)
    charge()
    

#charge()
    
#sub_follow_wall()
    
#wall_follow()

right_wheel.set_power(0)
left_wheel.set_power(0)
#arm_motor.set_position(30)

print("done!")
