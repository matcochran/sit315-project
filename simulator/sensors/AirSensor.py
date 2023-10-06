from . import IoTSensor

class AirSensor(IoTSensor):
    """Measures air temperature, humidity, and CO2 concentration."""
    def __init__(self) -> None:
        super().__init__(type="air")

    def generate_sensor_data(self):
        return {
            "temperature": self._r(-20, 50),
            "humidity": self._r(0, 100),
            "co2": self._r(300, 5000)  # ppm
        }
