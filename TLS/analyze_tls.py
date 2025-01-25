import pyshark
import matplotlib.pyplot as plt
from collections import Counter

def analyze_pcap(file_path):
    """
    Analyze the captured .pcap file for MQTT performance metrics over TLS.
    """
    print(f"Analyzing {file_path}...")
    cap = pyshark.FileCapture(file_path, display_filter='tcp.port == 8883')  # Filter for TLS traffic on port 8883
    packet_count = 0
    mqtt_count = 0
    timestamps = []
    packet_sizes = []
    total_data = 0

    for packet in cap:
        packet_count += 1
        try:
            # Since packets are encrypted, we cannot analyze MQTT directly.
            # However, we can analyze general packet metrics like packet size and timestamps.
            if 'TLS' in packet:
                mqtt_count += 1  # Count TLS packets (presumably MQTT over TLS)
                timestamps.append(packet.sniff_time.timestamp())
                packet_sizes.append(int(packet.length))
                total_data += int(packet.length)
        except AttributeError:
            continue

    cap.close()

    # Performance Metrics
    duration = max(timestamps) - min(timestamps) if len(timestamps) > 1 else 0
    latencies = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    throughput = len(timestamps) / duration if duration > 0 else 0

    # Plot Latency Distribution
    if latencies:
        plt.figure(figsize=(10, 5))
        plt.hist(latencies, bins=20, color='blue', edgecolor='black')
        plt.title("Latency Distribution")
        plt.xlabel("Latency (seconds)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    # Plot Packet Size Distribution
    plt.figure(figsize=(10, 5))
    plt.hist(packet_sizes, bins=20, color='green', edgecolor='black')
    plt.title("Packet Size Distribution")
    plt.xlabel("Packet Size (bytes)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    # Summary Results
    print("=== Analysis Results ===")
    print(f"Total Packets Captured: {packet_count}")
    print(f"TLS Packets (Presumably MQTT over TLS): {mqtt_count}")
    print(f"Total Data Transferred: {total_data} bytes")
    print(f"Capture Duration: {duration:.2f} seconds")
    print(f"Average Latency: {sum(latencies)/len(latencies):.3f} seconds" if latencies else "No Latency Data")
    print(f"Throughput: {throughput:.2f} packets/second")

# Main function
if __name__ == "__main__":
    pcap_file = "tls.pcap"  # Replace with your .pcap file path
    analyze_pcap(pcap_file)

