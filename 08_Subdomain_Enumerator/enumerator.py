import argparse
import socket
import sys
import os
import time
import concurrent.futures

def resolve_subdomain(subdomain: str, domain: str):
    """Attempts to resolve a subdomain to an IP address."""
    target = f"{subdomain}.{domain}"
    try:
        # If the subdomain exists, this will return its IP address
        ip = socket.gethostbyname(target)
        return target, ip
    except socket.gaierror:
        # The subdomain does not exist (DNS resolution failed)
        return None

def main():
    parser = argparse.ArgumentParser(description="Fast OSINT Subdomain Enumerator")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the subdomain wordlist")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of concurrent threads (default: 50)")
    parser.add_argument("-o", "--output", help="Save discovered subdomains to a text file")

    args = parser.parse_args()

    # Verify wordlist exists
    if not os.path.isfile(args.wordlist):
        print(f"[-] Error: Wordlist '{args.wordlist}' not found.")
        sys.exit(1)

    # Read the wordlist
    with open(args.wordlist, 'r', encoding='utf-8') as f:
        # Strip newlines and ignore empty lines
        subdomains = [line.strip() for line in f if line.strip()]

    print("="*60)
    print("🌍 OSINT Subdomain Enumerator")
    print("="*60)
    print(f"[*] Target Domain : {args.domain}")
    print(f"[*] Wordlist      : {args.wordlist} ({len(subdomains)} words)")
    print(f"[*] Threads       : {args.threads}")
    print("="*60)
    print("[*] Starting enumeration... Please wait.\n")

    start_time = time.time()
    discovered = []

    # Using ThreadPoolExecutor for modern, clean multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Map the resolve_subdomain function to all subdomains in the list
        futures = {executor.submit(resolve_subdomain, sub, args.domain): sub for sub in subdomains}
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                target_url, ip_address = result
                print(f"[+] Discovered : {target_url:<25} | IP: {ip_address}")
                discovered.append(result)

    elapsed_time = round(time.time() - start_time, 2)

    print("\n" + "="*60)
    print(f"[*] Enumeration completed in {elapsed_time} seconds.")
    print(f"[*] Total subdomains found: {len(discovered)}")

    # Save to file if output is specified
    if args.output and discovered:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"Subdomain enumeration results for {args.domain}\n")
                f.write("="*45 + "\n")
                for url, ip in sorted(discovered):
                    f.write(f"{url} - {ip}\n")
            print(f"[+] Results safely saved to '{args.output}'")
        except Exception as e:
            print(f"[-] Error saving to file: {e}")

if __name__ == "__main__":
    main()
