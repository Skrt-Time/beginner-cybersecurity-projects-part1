import socket
import argparse
import threading
from queue import Queue
import time
import sys

# Lock for thread-safe printing
print_lock = threading.Lock()

# Common port mapping for better output formatting
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS", 
    80: "HTTP", 110: "POP3", 139: "NetBIOS", 143: "IMAP", 
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"
}

def grab_banner(ip: str, port: int, timeout: float) -> str:
    """Attempts to grab the service banner from an open port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        
        # Send a dummy HTTP request just in case it's a web server waiting for input
        if port in [80, 443, 8080]:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        
        # Receive the banner
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        
        # Clean up the banner (remove newlines for clean printing)
        return banner.split('\n')[0] if banner else "No banner received"
    except Exception:
        return "No banner (timeout or connection reset)"

def scan_port(target: str, port: int, open_ports: list, timeout: float, banner_grab: bool):
    """Attempts to connect to a specific port on the target."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target, port))
        
        if result == 0:
            service_name = COMMON_PORTS.get(port, "Unknown")
            output_msg = f"[+] Port {port:<5} | {service_name:<10} | OPEN"
            
            banner_info = ""
            if banner_grab:
                banner_info = grab_banner(target, port, timeout)
                output_msg += f" | Banner: {banner_info}"
            
            with print_lock:
                print(output_msg)
                
            open_ports.append((port, service_name, banner_info))
            
        s.close()
    except Exception:
        pass

def threader(target: str, q: Queue, open_ports: list, timeout: float, banner_grab: bool):
    """Worker thread function."""
    while True:
        worker = q.get()
        scan_port(target, worker, open_ports, timeout, banner_grab)
        q.task_done()

def parse_ports(port_arg: str) -> list:
    """Parses the port argument from the CLI."""
    ports = []
    try:
        if '-' in port_arg:
            start, end = map(int, port_arg.split('-'))
            ports = list(range(start, end + 1))
        elif ',' in port_arg:
            ports = [int(p) for p in port_arg.split(',')]
        else:
            ports = [int(port_arg)]
        return ports
    except ValueError:
        print("[-] Error: Invalid port format. Use '80', '22,80,443', or '1-1024'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Advanced Python Port Scanner (Nmap alternative)")
    parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="1-1024", help="Ports to scan (default: 1-1024)")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("-sV", "--service-version", action="store_true", help="Attempt to grab service banners")
    parser.add_argument("-o", "--output", help="Save results to a text file")

    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[-] Error: Could not resolve hostname '{args.target}'.")
        sys.exit(1)

    ports_to_scan = parse_ports(args.ports)
    open_ports = []

    print("="*75)
    print("🔍 Advanced Python Port Scanner")
    print("="*75)
    print(f"[*] Target      : {args.target} ({target_ip})")
    print(f"[*] Ports       : {args.ports} ({len(ports_to_scan)} ports)")
    print(f"[*] Threads     : {args.threads}")
    print(f"[*] Timeout     : {args.timeout}s")
    print(f"[*] Banner Grab : {'Enabled' if args.service_version else 'Disabled'}")
    print("="*75)
    
    start_time = time.time()
    
    q = Queue()
    
    for _ in range(args.threads):
        t = threading.Thread(target=threader, args=(target_ip, q, open_ports, args.timeout, args.service_version))
        t.daemon = True
        t.start()
        
    for port in ports_to_scan:
        q.put(port)
        
    q.join()
    
    elapsed = round(time.time() - start_time, 2)
    
    print("="*75)
    print(f"[*] Scan completed in {elapsed} seconds.")
    print(f"[*] Total open ports found: {len(open_ports)}")

    if args.output and open_ports:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"Scan results for {args.target} ({target_ip})\n")
            f.write("="*60 + "\n")
            for p, s, b in sorted(open_ports):
                line = f"Port {p:<5} | {s:<10} | OPEN"
                if args.service_version and b:
                    line += f" | Banner: {b}"
                f.write(line + "\n")
        print(f"[+] Results safely saved to '{args.output}'")

if __name__ == "__main__":
    main()
