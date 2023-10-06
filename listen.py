import paho.mqtt.client as mqtt


BROKER_HOST = "a6ee3ad5494ff4ceeaebbe05b32aea36-633398894.us-east-1.elb.amazonaws.com"
BROKER_PORT = 1883
USERNAME = ""
PASSWORD = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")  # Subscribe to all topics; resubscribe on reconnect

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}\nPayload: {msg.payload.decode('utf-8')}\n")

if __name__ == "__main__":
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, 60)

    client.loop_forever()
