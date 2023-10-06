import random
from . import IoTSensor


class WindSensor(IoTSensor):
    """Measures wind speed, direction, and gusts."""
    def __init__(self) -> None:
        super().__init__(type="wind")

    def generate_sensor_data(self):
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        return {
            "speed": self._r(0, 150),
            "direction": random.choice(directions),
        }