'''
Test script to continuously display the output of the two IR sensors.
> Jan.23
'''

from gpiozero import DistanceSensor
from time import sleep

config = {
    'sensor_1': {
        'echo': 12,
        'trigger': 23,
    },
    'sensor_2': {
        'echo': 16,
        'trigger': 24,
    },
    'max_dist': 4,
}
if __name__ == '__main__':

    # Init distance sensors:
    # echo, trigger
    sensor_1 = DistanceSensor(config['sensor_1']['echo'],
                              config['sensor_1']['trigger'],
                              max_distance=config['max_dist'])
    sensor_2 = DistanceSensor(config['sensor_2']['echo'],
                              config['sensor_2']['trigger'],
                              max_distance=config['max_dist'])

    # Use cache:
    cache = {1: None, 2: None}

    d1, d2 = 0, 0
    while True:
        d1 = sensor_1.distance
        sleep(0.1)
        d2 = sensor_2.distance
        sleep(0.1)
        print(f'd1: {d1:.1f} m\td2: {d2:.1f} m')
