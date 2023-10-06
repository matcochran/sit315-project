from . import IoTSensor


class WaterLevelSensor(IoTSensor):
    """Measures water level, temperature, and turbidity."""
    def __init__(self) -> None:
        super().__init__(type="water_level")

    def generate_sensor_data(self):
        return {
            "level": self._r(0, 100),
            "temperature": self._r(0, 40),
            "turbidity": self._r(0, 1000)  # NTU (Nephelometric Turbidity Units)
        }
    