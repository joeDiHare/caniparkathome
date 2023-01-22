'''
Test script to continuously display the output of the two IR sensors.
> Jan.23
'''

from gpiozero import DistanceSensor
from time import sleep


if __name__ == '__main__':

    # Init distance sensors:
    sensor_1 = DistanceSensor(23, 24, max_distance=4)
    sensor_2 = DistanceSensor(27, 22, max_distance=4)

    # Use cache:
    cache = {1: None, 2: None}

    d1, d2 = 0, 0
    while True:
        d1 = sensor_1.distance
        sleep(0.1)
        d2 = sensor_2.distance
        sleep(0.1)
        print(f'd1: {d1:.1f} m\td2: {d2:.1f} m')
