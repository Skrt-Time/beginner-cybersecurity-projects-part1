# 02 - Network Packet Sniffer

A command-line network packet sniffer built with Python and the `scapy` library. This tool captures network traffic in real-time, extracts key information (IP addresses, protocols, ports), and allows users to save the captured traffic into a PCAP file for further analysis in tools like Wireshark.

## ⚠️ Educational Disclaimer
**This tool is strictly for educational and ethical use.** Sniffing network traffic can expose sensitive, unencrypted data. Only run this tool on networks and devices you own, or where you have explicit authorization. Unauthorized packet sniffing is illegal.

## ✨ Key Features
* **Real-time Capture:** Monitors and displays live network traffic (TCP, UDP, ICMP).
* **BPF Filtering:** Supports Berkeley Packet Filter (BPF) syntax to capture specific traffic (e.g., only HTTP traffic or specific IP addresses).
* **PCAP Export:** Ability to save captured packets to a `.pcap` file for deep-dive analysis.
* **Packet Limiter:** Configure exactly how many packets you want to capture before automatically stopping.

## ⚙️ Prerequisites & Installation
This script requires the third-party `scapy` library and **Administrator/root privileges** to listen to network interfaces.

Install the required Python library using pip:
```bash
pip install scapy
```

## 📖 Help Menu
You can access the built-in manual by running the `-h` or `--help` command:

```bash
python sniffer.py --help
```

**Output:**
```text
usage: sniffer.py [-h] [-i INTERFACE] [-c COUNT] [-f FILTER] [-o OUTPUT]

Basic Network Packet Sniffer using Scapy

options:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Network interface to sniff on (e.g., eth0, wlan0)
  -c COUNT, --count COUNT
                        Number of packets to capture (default: 0 = infinite)
  -f FILTER, --filter FILTER
                        BPF filter (e.g., 'tcp', 'icmp', 'port 80')
  -o OUTPUT, --output OUTPUT
                        Save captured packets to a PCAP file (e.g., capture.pcap)
```

## 💻 Command Examples
*(Note: On Linux/macOS, you must prefix these commands with `sudo`)*

### 1. Basic Sniffing
**Listen to all traffic on the default interface:**
```bash
python sniffer.py
```

**Listen to a specific interface (e.g., eth0):**
```bash
python sniffer.py -i eth0
```

### 2. Advanced Filtering and Exporting
**Capture only 50 ICMP (Ping) packets:**
```bash
python sniffer.py -f icmp -c 50
```

**Capture TCP traffic on port 80 (HTTP) and save it to a file:**
```bash
python sniffer.py -f "tcp port 80" -o http_traffic.pcap
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features could be implemented:
1. **Payload Extraction:** Add functionality to decode and display raw unencrypted payloads (like plain-text FTP or HTTP credentials).
2. **Colorized Output:** Implement libraries like `colorama` to highlight different protocols or suspicious traffic in different colors.
3. **MAC Address Resolution:** Map MAC addresses to their respective hardware vendors (OUI lookup).
