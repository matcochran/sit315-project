from dataclasses import dataclass, asdict
import json
from typing import Any, Dict, Union


@dataclass
class IoTSensorPayload:
    sensor_id: str
    sensor_type: str
    timestamp: float
    data: Dict[str, Union[str, float]]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(
            sensor_id=d['sensor_id'],
            sensor_type=d['sensor_type'],
            timestamp=d['timestamp'],
            data=d['data']
        )

    def to_json(self):
        return json.dumps(asdict(self))
