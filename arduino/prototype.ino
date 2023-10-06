#include <ArduinoJson.h>

const unsigned long startTime = 1672982400;

const int DHTPIN = 8;
volatile bool startReading = false;
const char* SENSOR_ID = "b97fb7c5-6f32-4db6-bfd2-2974792fe686";
const char* SENSOR_TYPE = "temp_humid";

void setup() {
  Serial.begin(9600);
  pinMode(DHTPIN, INPUT);
  // attachInterrupt(digitalPinToInterrupt(DHTPIN), handleInterrupt, RISING);
}

void loop() {
  // if (startReading) {
    float temperature, humidity;
    if (readDHT11Data(temperature, humidity)) {
      sendJSONData(temperature, humidity);
    }
    startReading = false;
  // }
}

// unused, because DHT11 requires a start signal
// void handleInterrupt() {
//   startReading = true;
// }

bool readDHT11Data(float &temperature, float &humidity) {
  // Start the data transmission by pulling the data pin LOW for 18 milliseconds.
  pinMode(DHTPIN, OUTPUT);
  digitalWrite(DHTPIN, LOW);
  delay(18);

  // Set the data pin to INPUT to read the response from the DHT11 sensor.
  pinMode(DHTPIN, INPUT);

  // Wait for the DHT11 to respond (acknowledge).
  unsigned int timeout = 10000;  // Maximum timeout for the sensor response.
  while (digitalRead(DHTPIN) == HIGH) {
    if (--timeout == 0) {
      return false;
    }
  }

  // Wait for the start of the data transmission (LOW signal).
  timeout = 10000;  // Maximum timeout for the start signal.
  while (digitalRead(DHTPIN) == LOW) {
    if (--timeout == 0) {
      return false;
    }
  }

  // Wait for the end of the start signal (HIGH signal).
  timeout = 10000;  // Maximum timeout for the end of start signal.
  while (digitalRead(DHTPIN) == HIGH) {
    if (--timeout == 0) {
      return false;
    }
  }

  // Read 40 bits of data from the sensor (5 bytes).
  uint8_t data[5] = {0};
  for (int i = 0; i < 5; i++) {
    data[i] = readByte();
  }

  // Check the checksum to verify the data integrity.
  uint8_t checksum = data[0] + data[1] + data[2] + data[3];

  int rawHumidity = data[0];
  int rawTemperature = data[2];

  humidity = static_cast<float>(rawHumidity);
  temperature = static_cast<float>(rawTemperature);
  return (data[4] == checksum);
}

// in lieu of a wifi connection, we just print to the serial output
void sendJSONData(float temperature, float humidity) {
  StaticJsonDocument<200> payload;
  payload["sensor_id"] = SENSOR_ID;
  payload["type"] = SENSOR_TYPE;
  payload["timestamp"] = startTime + millis() / 1000;

  JsonObject data = payload.createNestedObject("data");
  data["temperature"] = temperature;
  data["humidity"] = humidity;

  serializeJson(payload, Serial);
  Serial.println();
}

// Function to read a single byte from the DHT11 sensor.
uint8_t readByte() {
  uint8_t value = 0;
  for (int i = 0; i < 8; i++) {
    // Wait for the start of a bit.
    while (digitalRead(DHTPIN) == LOW);

    // Wait for the end of the bit (data signal).
    unsigned long startTime = micros();
    while (digitalRead(DHTPIN) == HIGH);
    unsigned long duration = micros() - startTime;

    // Check the duration to determine the bit value.
    if (duration > 40) {
      value |= (1 << (7 - i));
    }
  }
  return value;
}
