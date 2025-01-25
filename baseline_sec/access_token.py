
import paho.mqtt.client as mqtt
import time, json, math
from sense_hat import SenseHat

# Configuration
TOKEN = "......"  # Your secret token
HOST = "......."  # ThinkBoard server
PORT = 1883 # Port for MQTT
TOPIC = "v1/devices/me/telemetry"

# Initialize Sense HAT
sense = SenseHat()

# Counters
total_sent = 0
total_acknowledged = 0

# Callback when connected
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Callback for successful PUBACK
def on_publish(client, userdata, mid):
    global total_acknowledged
    total_acknowledged += 1
    print(f"PUBACK received for Message ID: {mid}")  # Added debug statement

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish  # Attach the modified callback
client.username_pw_set(TOKEN)
client.connect(HOST, PORT, 60)
client.loop_start()

# Publishing data
try:
    while True:
        # Capture temperature and shaking data
        acc_list = []
        for _ in range(10):
            raw_acc = sense.get_accelerometer_raw()
            x, y, z = raw_acc['x'], raw_acc['y'], raw_acc['z']
            acc_magnitude = math.sqrt(x * x + y * y + z * z)
            acc_list.append(acc_magnitude)
            time.sleep(0.2)

        temperature = round(sense.get_temperature(), 2)
        shaking = round((max(acc_list) - min(acc_list)) * 7, 2)

        # Prepare the payload
        payload = {"temperature": temperature, "shaking": shaking}
        result = client.publish(TOPIC, json.dumps(payload), qos=1)
        print(f"Published: {payload} (Message ID: {result.mid})")

        total_sent += 1
        time.sleep(2)

except KeyboardInterrupt:
    print("\nTest Stopped")
    print(f"Total Messages Sent: {total_sent}")
    print(f"Total Acknowledged (PUBACK): {total_acknowledged}")
    print(f"Packet Loss: {total_sent - total_acknowledged} messages")
finally:
    client.disconnect()
    print("Disconnected from MQTT broker.")

