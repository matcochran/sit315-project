from . import IoTSensor


class PHSensor(IoTSensor):
    """Measures pH of the water and its temperature."""
    def __init__(self) -> None:
        super().__init__(type="ph")

    def generate_sensor_data(self):
        return {
            "ph": self._r(0, 14),
            "temperature": self._r(0, 40)
        }
    