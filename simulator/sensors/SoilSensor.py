from . import IoTSensor


class SoilSensor(IoTSensor):
    """Measures soil moisture, pH, temperature, and salinity."""
    def __init__(self) -> None:
        super().__init__(type="soil")

    def generate_sensor_data(self):
        return {
            "moisture": self._r(0, 100),  # moisture in percentage
            "ph": self._r(0, 14),
            "temperature": self._r(0, 50),  # temperature in °C
            "salinity": self._r(0, 1000)  # salinity in ppm
        }