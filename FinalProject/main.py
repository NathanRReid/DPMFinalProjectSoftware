from utils.brick import BP, Motor, TouchSensor, wait_ready_sensors, SensorError
from utils.sound import Sound
import time, math

FORWARD_SPEED = 20
SENSOR_POLL_SLEEP = 0.25

tone1 = Sound(duration=1.0, volume=80, pitch="A4")
tone2 = Sound(duration=1.0, volume=80, pitch="B4")
tone3 = Sound(duration=1.0, volume=80, pitch="C5")
tone4 = Sound(duration=1.0, volume=80, pitch="D5")

T_SENSOR1 = TouchSensor(1)
T_SENSOR2 = TouchSensor(2)
T_SENSOR3 = TouchSensor(3)

MOTOR = Motor("A")
MOTOR.set_position_relative(0)
print("Initializing")
time.sleep(0.5)
motorstatus=False
try:    
    wait_ready_sensors()

    while True:
        try:
            if (T_SENSOR1.is_pressed() and T_SENSOR2.is_pressed() and T_SENSOR3.is_pressed()):
                print("Emergency Stop")
                MOTOR.set_power(0)
                MOTOR.reset_encoder()
                BP.reset_all()
                motorstatus=False
                break

            elif (T_SENSOR2.is_pressed() and T_SENSOR3.is_pressed()):
                    motorstatus=True
            
            if motorstatus:
                    MOTOR.set_position_relative(60)
                    time.sleep(0.1)
                    MOTOR.set_position(0)
                    time.sleep(0.1)
                    
            time.sleep(0.1)
            if (T_SENSOR1.is_pressed() and T_SENSOR2.is_pressed() and not T_SENSOR3.is_pressed()):
                tone4.play()
                time.sleep(0.1)
            elif (T_SENSOR1.is_pressed() and not T_SENSOR2.is_pressed() and not T_SENSOR3.is_pressed()):
                tone1.play()
                time.sleep(0.1)

            elif (T_SENSOR2.is_pressed() and not T_SENSOR1.is_pressed() and not T_SENSOR3.is_pressed()):
                tone2.play()
                time.sleep(0.1)

            elif (T_SENSOR3.is_pressed() and not T_SENSOR2.is_pressed() and not T_SENSOR1.is_pressed()):
                tone3.play()
                time.sleep(0.1)
                
            

        except SensorError as error:
            MOTOR.set_power(0)
            BP.reset_all()
            print(error)
            exit()
    
        time.sleep(SENSOR_POLL_SLEEP)

except KeyboardInterrupt:
    MOTOR.set_power(0)
    BP.reset_all()
    
