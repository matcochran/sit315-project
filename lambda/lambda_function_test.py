from dataclasses import dataclass, asdict, field
import json
import logging
from typing import Dict, Union, Any

import boto3
from pymongo import MongoClient


MONGO_CONNECTION_STRING = ""
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/379524012753/iot-data.fifo"
 
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

def validate_payload(payload: Dict[str, Any]) -> bool:
    try:
        IoTSensorPayload.from_dict(payload)
        return True
    except (KeyError, TypeError):
        return False

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Processing unit starting.")
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client.iot
    collection = db.sensor_data

    sqs = boto3.client('sqs')

    messages = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10
    )

    processed_messages = 0
    invalid_messages = 0

    if 'Messages' in messages:
        for message in messages['Messages']:
            data = json.loads(message['Body'])
            logger.info(f"Processing message with data: {data}")

            if validate_payload(data):
                collection.insert_one(data)
                logger.info(f"Inserted data into MongoDB: {data}")
                processed_messages += 1
            else:
                logger.warning(f"Invalid payload detected: {data}")
                invalid_messages += 1

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

    logger.info("Processing unit ending.")
    return {
        'statusCode': 200,
        'body': f"Processed {processed_messages} valid messages. {invalid_messages} messages were invalid."
    }
