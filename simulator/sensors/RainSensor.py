from . import IoTSensor


class RainSensor(IoTSensor):
    """Measures rainfall quantity and rate."""
    def __init__(self) -> None:
        super().__init__(type="rain")

    def generate_sensor_data(self):
        return {
            "rainfall": self._r(0, 50),  # rainfall in mm
            "rate": self._r(0, 10)  # rainfall rate in mm/h
        }