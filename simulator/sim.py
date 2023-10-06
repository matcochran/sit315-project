import argparse
import multiprocessing
import random
from sensors import *

DEBUG = False
NUM_SENSORS_DEFAULT = 1
SEND_INTERVAL_RANGE_DEFAULT = (1, 10)

sensors = [
    SoilSensor,
    WindSensor,
    AirSensor,
    PHSensor,
    WaterLevelSensor,
    RainSensor,
    LightSensor,
]

def start_sensor_simulation(low: int = SEND_INTERVAL_RANGE_DEFAULT[0], high: int = SEND_INTERVAL_RANGE_DEFAULT[1], flat: int = None) -> None:
    sensor = random.choice(sensors)()
    if flat:
        sensor.simulate(interval_seconds=flat, debug=DEBUG)
    else:
        sensor.simulate(interval_seconds=random.randint(low, high), debug=DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start sensor simulations.")
    parser.add_argument('--sensors', type=int, default=NUM_SENSORS_DEFAULT,
                        help=f"Number of sensors to simulate. Default: {NUM_SENSORS_DEFAULT}")
    parser.add_argument('--interval', type=int, default=None,
                        help=f"Interval in seconds to send sensor data. Default: random between {SEND_INTERVAL_RANGE_DEFAULT[0]} and {SEND_INTERVAL_RANGE_DEFAULT[1]}")
    args = parser.parse_args()

    processes = []
    for _ in range(args.sensors):
        process = multiprocessing.Process(target=start_sensor_simulation, args=(SEND_INTERVAL_RANGE_DEFAULT[0], SEND_INTERVAL_RANGE_DEFAULT[1], args.interval))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
