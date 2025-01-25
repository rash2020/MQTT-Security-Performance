import paho.mqtt.client as mqtt
import time
import json
import math
from sense_hat import SenseHat
import ssl

# Configuration
TOKEN = "....."  # Replace with your ThingsBoard device token
HOST = "......"  # Replace with your ThingsBoard domain
PORT = 8883  # Secure MQTT Port
TOPIC = "v1/devices/me/telemetry"

# Path to certificates
CERT_PATH = "fullchain.pem"

# Initialize Sense HAT
sense = SenseHat()

# Counters for telemetry messages
total_sent = 0
total_acknowledged = 0

# Callback when connected
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to ThingsBoard!")
    else:          
        print(f"Connection failed with result code {rc}")

# Callback for PUBACK (QoS 1 confirmation)
def on_publish(client, userdata, mid):
    global total_acknowledged
    total_acknowledged += 1
    print(f"PUBACK received for Message ID: {mid}")

# Callback for disconnect
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection. Reconnecting...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"Reconnection failed: {e}")

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Set device token for authentication
client.username_pw_set(TOKEN)

# Configure TLS (SSL) for secure communication
client.tls_set(
    ca_certs=CERT_PATH,  # Path to the full chain certificate
    certfile=None,  # Not required for client authentication
    keyfile=None,  # Not required for client authentication
    cert_reqs=ssl.CERT_REQUIRED,  # Verify server certificate
    tls_version=ssl.PROTOCOL_TLSv1_2  # Use TLS 1.2
)

# Connect to the MQTT broker (ThingsBoard)
try:
    client.connect(HOST, PORT, 60)
    client.loop_start()  # Start a background loop to handle networking
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

# Publish telemetry data
try:
    while True:
        # Collect accelerometer data
        acc_list = []
        for _ in range(10):  # Collect 10 readings
            raw_acc = sense.get_accelerometer_raw()
            x, y, z = raw_acc["x"], raw_acc["y"], raw_acc["z"]
            acc_magnitude = math.sqrt(x * x + y * y + z * z)  # Calculate magnitude
            acc_list.append(acc_magnitude)
            time.sleep(0.2)  # Small delay between readings

        # Get temperature reading
        temperature = round(sense.get_temperature(), 2)

        # Calculate "shaking" metric
        shaking = round((max(acc_list) - min(acc_list)) * 7, 2)

        # Prepare telemetry payload
        payload = {"temperature": temperature, "shaking": shaking}

        # Publish data to ThingsBoard
        result = client.publish(TOPIC, json.dumps(payload), qos=1)
        print(f"Published: {payload} (Message ID: {result.mid})")

        total_sent += 1
        time.sleep(2)  # Wait before sending the next message

except KeyboardInterrupt:
    # Graceful exit on user interruption
    print("\nStopped by user")
    print(f"Total Messages Sent: {total_sent}")
    print(f"Total Acknowledged (PUBACK): {total_acknowledged}")
    print(f"Packet Loss: {total_sent - total_acknowledged} messages")
finally:
    # Disconnect the client
    client.disconnect()
    print("Disconnected from MQTT broker.")
