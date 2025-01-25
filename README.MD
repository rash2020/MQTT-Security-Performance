# MQTT Security and Performance Evaluation

This repository contains the code and scripts for evaluating the security and performance of MQTT communication in IoT systems. The experiments include baseline security tests,TLS-based secured setups and simulated attacks, and .

## Project Structure

```
.
├── TLS
│   ├── Tls_client.py         # Client implementation with TLS encryption
│   └── analyze_tls.py        # Script to analyze TLS traffic
├── attacks
│   ├── baseline_dos.py       # Script to simulate Denial of Service (DoS) attacks
│   ├── fake_handshakes.py    # Script to simulate fake handshake attacks
│   └── msg_attack.py         # Script for fake messages attacks
└── baseline_sec
    ├── access_token.py       # MQTT client using access token authentication
    ├── analyze_pcap.py       # Script to analyze captured packets
    └── mqtt_cred.py          # MQTT client using username-password authentication
```

## Requirements

- **Python 3.x** (Ensure it’s installed on your system)
- **Required Libraries**:
  - `paho-mqtt`
  - `scapy`
  - `pyshark`
- **IoT Broker**: The experiments require an MQTT broker such as [ThingsBoard](https://thingsboard.io).

## Usage Instructions

### 1. **Baseline Security Tests**
- Navigate to the `baseline_sec` directory.
- Run:
  - `access_token.py` for experiments using access tokens.
  - `mqtt_cred.py` for experiments using username-password credentials.

### 2. **Attack Simulations**
- Navigate to the `attacks` directory.
- Run the respective scripts:
  - `baseline_dos.py` to simulate a DoS attack.
  - `fake_handshakes.py` to simulate fake handshake attacks.
  - `msg_attack.py` to stimulate fake MQTT messages.

### 3. **TLS Setup**
- Navigate to the `TLS` directory.
- Run:
  - `Tls_client.py` to publish MQTT messages with TLS encryption.
  - `analyze_tls.py` to evaluate performance metrics for TLS-enabled communication.

## Results

The experimental results and analysis are included in the accompanying project report. Refer to the respective Python scripts for implementation details.

