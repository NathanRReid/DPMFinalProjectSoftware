from utils.brick import BP, Motor, EV3ColorSensor, EV3UltrasonicSensor, wait_ready_sensors, SensorError
import time, math


# Initialize motors with reverse orientation
left_wheel = Motor("A")
right_wheel = Motor("B")
arm_motor = Motor("D")

# Initialize sensors
color_sensor_down = EV3ColorSensor(2)  # Color sensor facing the ground
color_sensor_up = EV3ColorSensor(3)
ultra = EV3UltrasonicSensor(1)  # Assuming ultrasound on port 3

# Ensure sensors are ready before starting
wait_ready_sensors(True)

# Constants for motor power levels and walking intervals
WHEEL_POWER = -30  # Reversed for wheel orientation
ARM_POSITION = -30  # Reversed for arm positioning
arm_motor.set_limits(power=30)  # Lower power

def walk():
    """
    Basic walking function: moves forward and backward in short steps.
    """
    for _ in range(5):  # Perform 5 walking steps as an example
        # Move forward
        left_wheel.set_power(WHEEL_POWER)
        right_wheel.set_power(WHEEL_POWER)
        time.sleep(0.5)

        # Stop briefly
        left_wheel.set_power(0)
        right_wheel.set_power(0)
        time.sleep(0.2)

        # Move backward
        left_wheel.set_power(-WHEEL_POWER)
        right_wheel.set_power(-WHEEL_POWER)
        time.sleep(0.5)

        # Stop briefly again
        left_wheel.set_power(0)
        right_wheel.set_power(0)
        time.sleep(0.2)

RED_THRESHOLD = 100
BLUE_THRESHOLD = 50

def detect_red(rgb):
    r, g, b = rgb
    return r > (RED_THRESHOLD * (r + b + g)/380) and r > g*1.5 and r > b*1.5
def detect_blue(rgb):
    r, g, b = rgb
    return b > (BLUE_THRESHOLD * (r + b + g)/380) and b > g and b > r*1.5

def follow_red_line():
    """
    Line-following function using the color sensor to detect a red line and adjust direction.
    """
    # Read the color detected by the ground-facing sensor
    
    rgb_down = color_sensor_down.get_rgb()
    rgb_up = color_sensor_up.get_rgb()
    
    blue_d = detect_blue(rgb_down)
    blue_u = detect_blue(rgb_up)
    
    red_d = detect_red(rgb_down)
    red_u = detect_red(rgb_up)
    
    right_correction = (rgb_down[0] / (rgb_down[0] + rgb_down[1] + rgb_down[2] + 1))
    left_correction = (rgb_up[0] / (rgb_up[0] + rgb_up[1] + rgb_up[2] + 1))
    
    sum_corr = right_correction + left_correction + 0.005

    if blue_u:
        print("blue")
        left_wheel.set_power(-WHEEL_POWER*0.5)
        right_wheel.set_power(0)
        time.sleep(0.5)
    if blue_d:
        print("blue")
        left_wheel.set_power(-WHEEL_POWER)
        right_wheel.set_power(-WHEEL_POWER)
        time.sleep(0.5)
    else:
        # Move forward if on the red line
        left_wheel.set_power(WHEEL_POWER * ((2 * left_correction/sum_corr)))
        right_wheel.set_power(WHEEL_POWER * ((2 * right_correction/sum_corr)))

    # Brief delay to avoid overwhelming CPU
    print("dist: ", ultra.get_cm())
    print("color: ", rgb_up)
    time.sleep(0.1)

def kill():
    # Stop all motors on program exit
    left_wheel.set_power(0)
    right_wheel.set_power(0)
    arm_motor.set_power(0)

def block_check():
    dist = ultra.get_cm()
    r, g, b = color_sensor_up.get_rgb()
    
    past_dist = [255, 255, 255, 255, 255]
    past_dist.pop(0)
    past_dist.append(dist)
    
    is_orange = lambda r, g, b: 1.5 < r / g < 4 and 3 < r / b
    block_found = (min(past_dist) <= 17)
    print(past_dist)

    if (min(past_dist) <= 12) and (is_orange):
        kill()
        
        left_wheel.set_power(-WHEEL_POWER)
        right_wheel.set_power(-WHEEL_POWER)
        time.sleep(0.5)
        
        arm_motor.set_position(-90)
        time.sleep(1)  # Wait for the arm to reach the position
        
        left_wheel.set_power(WHEEL_POWER)
        right_wheel.set_power(WHEEL_POWER)
        time.sleep(2)

        left_wheel.set_power(0)
        right_wheel.set_power(0)
        arm_motor.set_position(0)
        time.sleep(1)  # Wait for the arm to reach the position
        

def moving():
    t = 0
    
    past_dist = [255, 255, 255, 255, 255]
    
    
    while (t < 100):
        dist = ultra.get_cm()
        past_dist.pop(0)
        past_dist.append(dist)
        
        block_check()
        
        if ((max(past_dist) - min(past_dist)) < 0.5) and not(min(past_dist) == 255):
            print('kill')
            left_wheel.set_power(-2 * WHEEL_POWER)
            right_wheel.set_power(-WHEEL_POWER)
            time.sleep(3)
        
        follow_red_line()
        t += 1


def move_arm_to_positions():
    try:
        print("move arm")
        # Move to -90 degrees
        arm_motor.set_position(-90)
        time.sleep(1)  # Wait for the arm to reach the position

        # Move back to 0 degrees
        arm_motor.set_position(0)
        time.sleep(1)  # Wait for the arm to reach the position

    except KeyboardInterrupt:
        print("dont move arm")

        arm_motor.set_power(0)  # Stop motor if interrupted



try:
    # Run the arm movement function
    #move_arm_to_positions()
    
    # Test walking function
    #walk()

    # Switch to line-following mode
    #follow_red_line()
    
    moving()
    
    # Stop all motors on program exit
    left_wheel.set_power(0)
    right_wheel.set_power(0)
    arm_motor.set_power(0)

except KeyboardInterrupt:
    # Stop all motors on program exit
    left_wheel.set_power(0)
    right_wheel.set_power(0)
    arm_motor.set_power(0)
