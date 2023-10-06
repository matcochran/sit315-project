import base64
import json

import boto3
import paho.mqtt.client as mqtt

MQTT_BROKER = "a6ee3ad5494ff4ceeaebbe05b32aea36-633398894.us-east-1.elb.amazonaws.com"
MQTT_PORT = 1883
MQTT_TOPIC = "#"
USERNAME = ""
PASSWORD = ""

AWS_REGION = "us-east-1"
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/379524012753/iot-data.fifo"

sqs = boto3.client('sqs', region_name=AWS_REGION)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Received message '{str(msg.payload)}' on topic '{msg.topic}' with QoS {msg.qos}")
    payload = json.loads(msg.payload)
    timestamp = payload.get("timestamp")
    sensor_id = payload.get("sensor_id")

    dedup_id = f"{sensor_id}-{timestamp}"
    
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=msg.payload.decode('utf-8'),
        MessageDeduplicationId=dedup_id,
        MessageGroupId=sensor_id,  # ensures per-sensor ordering
    )

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
