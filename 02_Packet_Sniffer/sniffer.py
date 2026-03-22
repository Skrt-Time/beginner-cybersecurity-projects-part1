import argparse
import sys
from datetime import datetime
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, wrpcap
except ImportError:
    print("[-] Error: 'scapy' library is not installed.")
    print("[*] Please install it using: pip install scapy")
    sys.exit(1)

# Global list to store captured packets if output file is specified
captured_packets = []

def process_packet(packet):
    """Callback function executed for each captured packet."""
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = packet[IP].proto
        size = len(packet)

        # Determine protocol type
        if TCP in packet:
            proto_name = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            details = f"Ports: {src_port} -> {dst_port}"
        elif UDP in packet:
            proto_name = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            details = f"Ports: {src_port} -> {dst_port}"
        elif ICMP in packet:
            proto_name = "ICMP"
            details = f"Type: {packet[ICMP].type}"
        else:
            proto_name = f"OTHER ({protocol})"
            details = "N/A"

        # Print formatted output
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {proto_name:4} | {ip_src:15} -> {ip_dst:15} | Size: {size} bytes | {details}")

        # Append to global list for PCAP saving
        captured_packets.append(packet)

def main():
    parser = argparse.ArgumentParser(description="Basic Network Packet Sniffer using Scapy")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on (e.g., eth0, wlan0)")
    parser.add_argument("-c", "--count", type=int, default=0, help="Number of packets to capture (default: 0 = infinite)")
    parser.add_argument("-f", "--filter", help="BPF filter (e.g., 'tcp', 'icmp', 'port 80')")
    parser.add_argument("-o", "--output", help="Save captured packets to a PCAP file (e.g., capture.pcap)")

    args = parser.parse_args()

    print("="*60)
    print("🌐 Python Network Packet Sniffer")
    print("="*60)
    print(f"[*] Interface : {args.interface if args.interface else 'Default'}")
    print(f"[*] Filter    : {args.filter if args.filter else 'None'}")
    print(f"[*] Count     : {args.count if args.count > 0 else 'Infinite'}")
    print(f"[*] Output    : {args.output if args.output else 'None'}")
    print("="*60)
    print("[*] Starting packet capture... Press Ctrl+C to stop.\n")

    try:
        # Start sniffing
        sniff(iface=args.interface, count=args.count, filter=args.filter, prn=process_packet, store=False)
    except PermissionError:
        print("\n[-] Error: You need root/Administrator privileges to sniff packets.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] Capture stopped by user.")
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")

    # Save to PCAP if requested
    if args.output and captured_packets:
        print(f"\n[*] Saving {len(captured_packets)} packets to {args.output}...")
        wrpcap(args.output, captured_packets)
        print("[+] File saved successfully.")

if __name__ == "__main__":
    main()
