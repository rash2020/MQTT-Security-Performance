import pyshark
import matplotlib.pyplot as plt
from collections import Counter

def analyze_pcap(file_path):
    """
    Analyze the captured .pcap file for MQTT performance metrics.
    """
    print(f"Analyzing {file_path}...")
    cap = pyshark.FileCapture(file_path)
    packet_count = 0
    mqtt_count = 0
    timestamps = []
    packet_sizes = []
    topics = Counter()
    total_data = 0

    for packet in cap:
        packet_count += 1
        try:
            if 'MQTT' in packet:
                mqtt_count += 1
                timestamps.append(packet.sniff_time.timestamp())
                packet_sizes.append(int(packet.length))
                total_data += int(packet.length)
                if hasattr(packet.mqtt, 'topic'):
                    topics[packet.mqtt.topic] += 1
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

    # Plot Topics
    if topics:
        labels, values = zip(*topics.most_common(5))
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color='orange')
        plt.title("Top MQTT Topics by Packet Count")
        plt.xlabel("Topics")
        plt.ylabel("Packet Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Summary Results
    print("=== Analysis Results ===")
    print(f"Total Packets Captured: {packet_count}")
    print(f"MQTT Packets: {mqtt_count}")
    print(f"Total Data Transferred: {total_data} bytes")
    print(f"Capture Duration: {duration:.2f} seconds")
    print(f"Average Latency: {sum(latencies)/len(latencies):.3f} seconds" if latencies else "No Latency Data")
    print(f"Throughput: {throughput:.2f} packets/second")
    print("Top Topics:")
    for topic, count in topics.most_common(5):
        print(f"  {topic}: {count} packets")

# Main function
if __name__ == "__main__":
    pcap_file = "mqtt_base.pcap"  # Replace with your .pcap file path
    analyze_pcap(pcap_file)

