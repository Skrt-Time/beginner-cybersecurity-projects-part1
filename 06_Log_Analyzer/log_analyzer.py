import argparse
import re
import sys
from collections import Counter

# A list of common keywords that indicate a failed authentication across various services
FAILURE_KEYWORDS = [
    "fail", "denied", "invalid", "error", 
    "incorrect", "unauthorized", "refused", "reject"
]

# Universal Regex to find any valid IPv4 address on a line
IP_REGEX = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

def parse_logs_intelligently(log_file: str) -> list:
    """Reads the log file and heuristically extracts IPs associated with failed actions."""
    suspicious_ips = []

    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
            for line_number, line in enumerate(file, 1):
                lower_line = line.lower()
                
                # Check if the line contains ANY of our failure keywords
                if any(keyword in lower_line for keyword in FAILURE_KEYWORDS):
                    # Find all IPv4 addresses on this specific failing line
                    found_ips = IP_REGEX.findall(line)
                    
                    # Add them to our suspicious list
                    for ip in found_ips:
                        suspicious_ips.append(ip)
                        
        return suspicious_ips
    except FileNotFoundError:
        print(f"[-] Error: Log file '{log_file}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"[-] Error: Permission denied. Try running with 'sudo'.")
        sys.exit(1)

def analyze_failures(failed_ips: list, threshold: int, output_file: str):
    """Analyzes the list of IPs and flags those exceeding the threshold."""
    if not failed_ips:
        print("[+] No suspicious activity found in the log file.")
        return

    # Count occurrences of each IP
    ip_counts = Counter(failed_ips)
    flagged_ips = {ip: count for ip, count in ip_counts.items() if count >= threshold}

    print("="*65)
    print("🛡️  Universal Brute-Force & Anomaly Detection Results")
    print("="*65)
    
    if not flagged_ips:
        print(f"[+] No IPs exceeded the alert threshold of {threshold} events.")
        print("="*65)
        return

    print(f"[!] WARNING: Found {len(flagged_ips)} malicious IP(s) exceeding threshold!")
    print("-" * 65)
    print(f"{'IP ADDRESS':<20} | {'SUSPICIOUS EVENTS':<20} | {'STATUS'}")
    print("-" * 65)

    for ip, count in sorted(flagged_ips.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip:<20} | {count:<20} | [FLAGGED]")

    print("="*65)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Suspicious IPs detected (Heuristic Analysis)\n")
                f.write("="*45 + "\n")
                for ip, count in sorted(flagged_ips.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{ip} - {count} suspicious events\n")
            print(f"[+] Flagged IPs safely saved to '{output_file}'")
        except Exception as e:
            print(f"[-] Error saving to output file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Universal Heuristic Log Analyzer")
    parser.add_argument("-f", "--file", required=True, help="Path to the log file")
    parser.add_argument("-t", "--threshold", type=int, default=3, help="Number of suspicious events before flagging an IP (default: 3)")
    parser.add_argument("-o", "--output", help="Save the list of flagged IPs to a text file")

    args = parser.parse_args()

    print(f"[*] Analyzing log file: {args.file}")
    print(f"[*] Alert Threshold   : >= {args.threshold} events")
    print(f"[*] Detection Mode    : Heuristic Keyword Matching")
    print(f"[*] Extracting suspicious events...\n")
    suspicious_ips = parse_logs_intelligently(args.file)
    analyze_failures(suspicious_ips, args.threshold, args.output)

if __name__ == "__main__":
    main()
