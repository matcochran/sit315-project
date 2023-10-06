from abc import ABC, abstractmethod
from random import uniform
import time
from uuid import uuid4
from typing import Dict, Any, Union

import paho.mqtt.client as mqtt

from models import IoTSensorPayload


class IoTSensor(ABC):
    MQTT_BROKER: str = "a6ee3ad5494ff4ceeaebbe05b32aea36-633398894.us-east-1.elb.amazonaws.com"
    MQTT_PORT: int = 1883
    USERNAME = ""
    PASSWORD = ""
    MQTT_TOPIC: str = "sensor"
    RECONNECTION_ATTEMPTS: int = 3

    def __init__(self, type: str) -> None:
        self.sensor_id: str = str(uuid4())
        self.mqtt_client: mqtt.Client = None  # self.setup_mqtt_client()
        self.sensor_type: str = type

    def setup_mqtt_client(self) -> mqtt.Client:
        """Setup and return the MQTT client."""
        client = mqtt.Client(client_id=self.sensor_id)
        client.username_pw_set(self.USERNAME, self.PASSWORD)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.connect(self.MQTT_BROKER, self.MQTT_PORT, keepalive=60)
        return client
    
    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict[str, int], rc: int) -> None:
        """Callback for when the client receives a CONNACK response from the server."""
        print(f"Connected with result code {str(rc)}")
        client.subscribe(self.MQTT_TOPIC)  # Subscribe to all topics

    def on_disconnect(self, client: mqtt.Client, userdata: Any, rc: int) -> None:
        """Reconnect logic for MQTT client."""
        attempts: int = 0
        while attempts < self.RECONNECTION_ATTEMPTS:
            try:
                print(f"Reconnection attempt {attempts + 1}")
                client.reconnect()
                print("Reconnected successfully!")
                return
            except Exception:
                attempts += 1
                time.sleep(2)
        print("Failed to reconnect after multiple attempts.")

    @abstractmethod
    def generate_sensor_data(self) -> Dict[str, Union[str, float]]:
        """Generate sensor data."""
        pass

    def generate_data(self) -> IoTSensorPayload:
        """Generate data specific to the sensor."""
        return IoTSensorPayload(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            timestamp=time.time(),
            data=self.generate_sensor_data(),
        )

    def get_data(self) -> str:
        """Compile and return sensor data."""
        payload = self.generate_data()
        return payload.to_json()
    
    def publish_data(self, debug: bool = False) -> None:
        data = self.get_data()
        if debug:
            print(data)
        else:
            print(f"Publishing data from {self.sensor_type} sensor with ID {self.sensor_id}")
            self.mqtt_client.publish(f"{self.MQTT_TOPIC}/{self.sensor_type}", data)

    def simulate(self, interval_seconds: int, debug: bool = False) -> None:
        """Simulate sensor readings by periodically generating and publishing data."""
        print(f"Simulating {self.sensor_type} sensor with ID {self.sensor_id}")
        while True:
            self.publish_data(debug)
            time.sleep(interval_seconds)

    def _r(self, min: int, max: int) -> float:
        """Generate a random float value between min and max."""
        return round(uniform(min, max), 2)