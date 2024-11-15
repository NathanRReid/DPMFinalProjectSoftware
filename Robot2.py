from utils.brick import BP, Motor, EV3ColorSensor, EV3UltrasonicSensor, \
    wait_ready_sensors, SensorError
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
WHEEL_SPEED = -30  # Reversed for wheel orientation
ARM_POSITION = -30  # Reversed for arm positioning
arm_motor.set_limits(power=30)  # Lower power
RW = 0.021
RB = 0.053
DISTTODEG = 180 / (math.pi * RW)
ORIENTTODEG = RB / RW


def MoveDistForward(dist):
    try:
        left_wheel.set_limits(100)
        right_wheel.set_limits(100)
        left_wheel.set_position(int(dist * DISTTODEG))
        right_wheel.set_position(int(dist * DISTTODEG))
        left_wheel.set_power(0)
        right_wheel.set_power(0)
    except:
        print("Error")

def Rotate(deg):
    try:
        left_wheel.set_limits(100)
        right_wheel.set_limits(100)
        left_wheel.set_position(int(deg * ORIENTTODEG))
        right_wheel.set_position(int(-deg * ORIENTTODEG))
        left_wheel.set_power(0)
        right_wheel.set_power(0)
    except:
        print("Error")



def angle_to_object(deg_speed):
    speed = math.pi * RW * deg_speed / 180

    # Get the distance to the object
    dist1 = ultra.get_cm()
    time.sleep(0.1)
    dist2 = ultra.get_cm()

    dist_travelled = 0.1 * speed

    # Calculate the angle to the object
    angle = math.acos((dist1 ** 2 - dist2 ** 2 - dist_travelled ** 2) / (
                2 * dist_travelled * dist2))
    angle = angle * 180 / math.pi  # Convert to degrees

    return angle


def track_object():
    deg_speed = WHEEL_SPEED

    while True:
        # Get the current distance and angle to the object
        dist = ultra.get_cm()  # Current distance to the object in cm
        angle = angle_to_object(deg_speed)  # Get the angle to the object

        # If the object is within 10 cm, stop the robot
        if dist < 10:
            left_wheel.set_dps(0)
            right_wheel.set_dps(0)
            print("Object reached. Stopping.")
            return

        # Scale the speed based on the distance, slowing down as it approaches
        deg_speed = max(WHEEL_SPEED * (dist / 100),
                    -10)  # Slow down as dist decreases

        # Calculate wheel speed adjustment for angle correction
        correction = angle * 5  # Proportional gain to adjust heading

        # Adjust left and right wheel speeds
        left_wheel.set_dps(deg_speed - correction)
        right_wheel.set_dps(deg_speed + correction)

        # Short delay to allow the robot to respond
        time.sleep(0.1)

        # Reset wheel speeds to prevent lingering speed
        left_wheel.set_dps(0)
        right_wheel.set_dps(0)


def capture_object():
    # Move the arm to the capture position
    arm_motor.set_position(ARM_POSITION)

    # Move forward to capture the object
    left_wheel.set_power(WHEEL_SPEED)
    right_wheel.set_power(WHEEL_SPEED)
    time.sleep(2)

    # Stop the robot
    left_wheel.set_power(0)
    right_wheel.set_power(0)

    # Move the arm back to the initial position
    arm_motor.set_position(0)

def determine_color():
    # Get the color from the color sensor
    color = color_sensor_down.get_color()

    # Print the color
    print("Color: ", color)

    # Return the color
    return color

def moving():
    return 0



try:
    # Run the arm movement function
    # move_arm_to_positions()

    # Test walking function
    # walk()

    # Switch to line-following mode
    # follow_red_line()

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
