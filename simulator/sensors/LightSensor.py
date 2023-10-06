from . import IoTSensor


class LightSensor(IoTSensor):
    """Measures light intensity and UV radiation."""
    def __init__(self) -> None:
        super().__init__(type="light")

    def generate_sensor_data(self):
        return {
            "intensity": self._r(0, 1000),  # light intensity in lumens
            "uv_index": self._r(0, 11)  # UV index scale (0-11)
        }
