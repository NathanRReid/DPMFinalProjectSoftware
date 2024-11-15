from utils.brick import BP, Motor, EV3ColorSensor, EV3UltrasonicSensor, wait_ready_sensors, SensorError
import time, math


rmotor = Motor("A")
lmotor = Motor("C")
armmotor = Motor("D")

rmotor.set_position_relative(0)
lmotor.set_position_relative(0)
armmotor.set_position_relative(0)
print("Initializing")
time.sleep(0.5)
motorstatus=False

rmotor.set_power(0)
lmotor.set_power(0)
armmotor.set_power(0)
rmotor.reset_encoder()
lmotor.reset_encoder()
armmotor.reset_encoder()
BP.reset_all()
