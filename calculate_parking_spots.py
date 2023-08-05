'''
Script to monitor at sensible intervals the max distance from two
IR sensors (used as proxy for parking spots being available) and 
send status to remote web app.
> Jan.23
'''

from gpiozero import DistanceSensor
from time import sleep
from datetime import datetime
import requests

THRESHOLD = 1  # Used to determine if a car is parked [meters]
BASE = "https://www.thebaywolves.com"
REMOTE = "caniparkathome/from-rpi/{}/"
print(f"Current Time: {datetime.now()}")

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


def update_values(nr_free_spots):
    '''Send changed status to remote via http.'''
    if nr_free_spots == 0:
        value = "No, sorry."
    else:
        nr = f"spot{'' if nr_free_spots==1 else 's'}" 
        value = f"Yes! {nr_free_spots} {nr} available."

    print(f'Send API values:\n"{value}"\n\n')
    try:
        url = f"{BASE}/{REMOTE.format(nr_free_spots)}"
        print(f"Response: {requests.get(url)}")

    except Exception as error:
        print(f"Error:\n{error}\n\n")


def go_to_sleep_till_next_measurement():
    '''Decide how long to sleep for. Used in between readings.'''
    dt = datetime.now()
    if dt.hour < 6:       # 0AM - 6AM: only hourly updates
        wait_for_min = 60 - dt.minute
    elif dt.hour < 14:    # 6AM - 2PM: 5-min updates
        wait_for_min = 5
    else:                 # 2PM - Midnight: 1-min updates
        wait_for_min = 1
    print(f'Next measurament in {wait_for_min} min.')
    sleep(wait_for_min * 60)


if __name__ == '__main__':

    # Init distance sensors:
    sensor_1 = DistanceSensor(config['sensor_1']['echo'],
                              config['sensor_1']['trigger'],
                              max_distance=config['max_dist'])
    sensor_2 = DistanceSensor(config['sensor_2']['echo'],
                              config['sensor_2']['trigger'],
                              max_distance=config['max_dist'])


    # Use cache:
    cache = {1: None, 2: None}

    while True:
        d1 = sensor_1.distance
        S1_free = int(d1 > THRESHOLD)
        sleep(0.5)
        d2 = sensor_2.distance
        S2_free = int(d2 > THRESHOLD)
        print(f'd1: {d1:.1f} m\td2: {d2:.1f} m')

        if cache[1] is None or cache[1] != S1_free or cache[2] != S2_free:
            cache = {1: S1_free, 2: S2_free}
            update_values(S1_free + S2_free)

        go_to_sleep_till_next_measurement()
