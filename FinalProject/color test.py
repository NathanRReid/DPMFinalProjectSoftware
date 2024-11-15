from utils.brick import wait_ready_sensors, EV3ColorSensor

color_down = EV3ColorSensor(2)
color_up = EV3ColorSensor(3)


wait_ready_sensors()


for i in range(10):
    print("down")
    print(color_down.get_ambient())
    print(color_down.get_red())
    print(color_down.get_rgb())
    
    print("up")
    print(color_up.get_ambient())
    print(color_up.get_red())
    print(color_up.get_rgb())
    
    print("")