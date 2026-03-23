import argparse
import sys
import socket
import concurrent.futures
import time
import difflib

# Advanced Homoglyph Dictionary
HOMOGLYPHS = {
    'a': ['4', '@', 'q', 'e', 'o'], 'b': ['8', '6', 'h'], 'c': ['e', 'o'],
    'd': ['cl', 'b'], 'e': ['3', 'c', 'a'], 'f': ['t'], 'g': ['q', '9', '6'],
    'h': ['b', 'n'], 'i': ['1', 'l', 'j', '!'], 'j': ['i', 'l'], 'k': ['lc'],
    'l': ['1', 'i', 'I'], 'm': ['rn', 'nn', 'n'], 'n': ['m', 'h', 'r'],
    'o': ['0', 'c', 'a'], 'p': ['q'], 'q': ['g', 'p', '9'], 'r': ['n', 'i'],
    's': ['5', '$', 'z'], 't': ['7', 'f', '+'], 'u': ['v', 'y'], 'v': ['u'],
    'w': ['vv', 'v'], 'x': ['%', 'y'], 'y': ['v', 'u', 'x'], 'z': ['2', 's']
}

KEYBOARD_MAPPING = {
    'q': ['w', 'a'], 'w': ['q', 'e', 's', 'a'], 'e': ['w', 'r', 'd', 's'],
    'r': ['e', 't', 'f', 'd'], 't': ['r', 'y', 'g', 'f'], 'y': ['t', 'u', 'h', 'g'],
    'u': ['y', 'i', 'j', 'h'], 'i': ['u', 'o', 'k', 'j'], 'o': ['i', 'p', 'l', 'k'],
    'p': ['o', 'l'], 'a': ['q', 'w', 's', 'z'], 's': ['a', 'w', 'e', 'd', 'x', 'z'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'], 'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'], 'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'], 'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'], 'z': ['a', 's', 'x'], 'x': ['z', 's', 'd', 'c'],
    'c': ['x', 'd', 'f', 'v'], 'v': ['c', 'f', 'g', 'b'], 'b': ['v', 'g', 'h', 'n'],
    'n': ['b', 'h', 'j', 'm'], 'm': ['n', 'j', 'k']
}

TLDS = ['.com', '.net', '.org', '.co', '.io', '.xyz', '.info', '.biz', '.ai', '.dev']

# Blue Team: List of highly targeted brands for the verification mode
PROTECTED_BRANDS = [
    "microsoft", "apple", "google", "amazon", "facebook", "netflix", 
    "paypal", "linkedin", "instagram", "github", "binance", "coinbase", 
    "twitter", "yahoo", "chase", "wellsfargo", "bankofamerica", "tesla"
]

def analyze_suspicious_domain(suspicious_domain: str):
    """Calculates string similarity to detect if a domain is spoofing a real brand."""
    if '.' not in suspicious_domain:
        print("[-] Please provide a full domain (e.g., rnicrosoft.com)")
        return

    base_name = suspicious_domain.rsplit('.', 1)[0].lower()
    
    print("\n[*] Initializing Algorithmic Similarity Analysis...")
    print(f"[*] Analyzing target: '{suspicious_domain}'")
    
    # Check for exact matches first
    if base_name in PROTECTED_BRANDS:
        print(f"\n[+] SAFE✅: '{suspicious_domain}' matches an official protected brand exactly.")
        return

    # Use difflib to find the closest matches based on Gestalt Pattern Matching
    # Cutoff at 0.75 means the strings must be at least 75% similar
    matches = difflib.get_close_matches(base_name, PROTECTED_BRANDS, n=3, cutoff=0.75)
    
    if matches:
        print("\n🚨 DANGER: PHISHING ATTEMPT DETECTED! 🚨")
        print("="*50)
        print(f"The domain '{suspicious_domain}' is highly suspicious.")
        print(f"Did you mean to visit one of these legitimate sites?")
        for match in matches:
            # Calculate exact percentage for the UI
            ratio = difflib.SequenceMatcher(None, base_name, match).ratio() * 100
            print(f" ╰──> {match}.com (Similarity: {ratio:.1f}%)")
        print("="*50)
        print("[!] Advice: DO NOT enter your credentials on this site!")
    else:
        print("\n[+] NEUTRAL: This domain does not closely resemble our list of protected brands.")
        print("    (Note: It could still be dangerous, but it is not a direct typosquatting of top brands).")

def generate_homoglyphs(domain_name: str) -> set:
    variations = set()
    for i, char in enumerate(domain_name):
        if char in HOMOGLYPHS:
            for sub in HOMOGLYPHS[char]:
                variations.add(domain_name[:i] + sub + domain_name[i+1:])
    return variations

def generate_keyboard_typos(domain_name: str) -> set:
    variations = set()
    for i, char in enumerate(domain_name):
        if char in KEYBOARD_MAPPING:
            for sub in KEYBOARD_MAPPING[char]:
                variations.add(domain_name[:i] + sub + domain_name[i+1:])
    return variations

def check_dns(domain: str):
    try:
        ip = socket.gethostbyname(domain)
        return domain, ip
    except socket.gaierror:
        return domain, None

def main():
    parser = argparse.ArgumentParser(description="Advanced Phishing Domain Generator & Verifier")
    
    # We use mutually exclusive group because you either Generate OR Verify
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Target legitimate domain to GENERATE typos for (e.g., example.com)")
    group.add_argument("-v", "--verify", help="Suspicious domain to VERIFY against protected brands (e.g., rnicrosoft.com)")
    
    parser.add_argument("-r", "--resolve", action="store_true", help="Perform DNS resolution (Only works with -d)")
    parser.add_argument("-o", "--output", help="Save the generated list to a text file (Only works with -d)")
    
    args = parser.parse_args()

    print("="*70)
    print("🎣 Advanced Phishing Domain Generator & Verifier")
    print("="*70)

    # -----------------------------------------
    # DEFENSIVE MODE: Verify a suspicious domain
    # -----------------------------------------
    if args.verify:
        analyze_suspicious_domain(args.verify)
        sys.exit(0)

    # -----------------------------------------
    # OFFENSIVE/CTI MODE: Generate Typosquatting
    # -----------------------------------------
    if args.domain:
        if '.' not in args.domain:
            print("[-] Error: Please provide a valid domain with a TLD (e.g., domain.com)")
            sys.exit(1)
            
        base_name, original_tld = args.domain.lower().rsplit('.', 1)
        original_tld = '.' + original_tld

        print(f"[*] Mode: CTI Generation")
        print(f"[*] Target Domain : {args.domain}\n")

        all_variations = set()
        for v in generate_homoglyphs(base_name): all_variations.add(v + original_tld)
        for v in generate_keyboard_typos(base_name): all_variations.add(v + original_tld)
        for tld in TLDS:
            if tld != original_tld: all_variations.add(base_name + tld)

        all_variations.discard(args.domain)
        domains_list = sorted(list(all_variations))

        print(f"[*] Total unique malicious combinations generated: {len(domains_list)}")

        if args.resolve:
            print("\n[+] Initiating DNS Resolution via Multithreading...")
            active_threats = []
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                future_to_domain = {executor.submit(check_dns, dom): dom for dom in domains_list}
                for future in concurrent.futures.as_completed(future_to_domain):
                    domain, ip = future.result()
                    if ip:
                        print(f" ╰──> 🚨 CRITICAL: {domain:<20} is ACTIVE! (IP: {ip})")
                        active_threats.append((domain, ip))
                        
            print(f"\n[*] Found {len(active_threats)} actively registered look-alike domains.")
        else:
            print("\n[*] Sample of generated domains:")
            for domain in domains_list[:10]:
                print(f" ╰──> {domain}")
            print("\n[!] Tip: Run with '--resolve' to check if hackers have already bought these domains!")

if __name__ == "__main__":
    main()
