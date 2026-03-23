# 08 - OSINT Subdomain Enumerator

A fast, multithreaded reconnaissance tool designed to uncover hidden subdomains of a target domain. Subdomain enumeration is a critical first step in the **OSINT (Open Source Intelligence)** gathering phase and Bug Bounty hunting, as it expands the attack surface by revealing forgotten or poorly secured infrastructure (like development servers or administrative panels).

## ⚠️ Educational Disclaimer
**This tool is strictly for educational and ethical use.** While making DNS queries is generally considered passive reconnaissance and is legal, you should only enumerate domains you own or have explicit authorization to test (such as Bug Bounty programs). Generating massive amounts of DNS traffic against a single target could be perceived as disruptive.

## ✨ Key Features
* **DNS Resolution:** Leverages standard DNS queries (`socket.gethostbyname`) to actively verify if a guessed subdomain is currently registered and pointing to an IP address.
* **Modern Multithreading:** Utilizes Python's `concurrent.futures.ThreadPoolExecutor` for high-performance, concurrent DNS lookups, drastically reducing scan times compared to sequential checking.
* **IP Mapping:** Not only discovers the subdomain but instantly resolves and displays its underlying IPv4 address.
* **Clean Data Export:** Easily save the list of discovered subdomains and their IP addresses to a `.txt` file for the next phase of the audit (e.g., port scanning).

## ⚙️ Prerequisites & Installation
This script is lightweight and uses **only Python's built-in standard libraries** (`socket`, `concurrent.futures`, `argparse`). No external `pip` installations or virtual environments are required.

### 🛡️ Note on Repository Maintenance (.gitignore)
If you are exporting your scan results using the `-o` flag, make sure these files are not uploaded to GitHub. Add `*.txt` to your global repository `.gitignore` file to prevent leaking reconnaissance data. *(A small dictionary `subdomains.txt` is provided in the repository for basic testing).*

## 📖 Help Menu
You can access the built-in manual by running the `-h` or `--help` command:

```bash
python enumerator.py --help
```

**Output:**
```text
usage: enumerator.py [-h] -d DOMAIN -w WORDLIST [-t THREADS] [-o OUTPUT]

Fast OSINT Subdomain Enumerator

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Target domain (e.g., example.com)
  -w WORDLIST, --wordlist WORDLIST
                        Path to the subdomain wordlist
  -t THREADS, --threads THREADS
                        Number of concurrent threads (default: 50)
  -o OUTPUT, --output OUTPUT
                        Save discovered subdomains to a text file
```

## 💻 Command Examples

### 1. Basic Enumeration
Test a target domain using the provided mini-wordlist:
*(Note: `google.com` is used here as an example since their DNS infrastructure handles millions of queries, but always prefer scanning your own domains).*
```bash
python enumerator.py -d google.com -w subdomains.txt
```

### 2. High-Speed Export Scan
Increase the thread count to 100 for faster processing of large wordlists and export the results:
```bash
python enumerator.py -d yourdomain.com -w subdomains.txt -t 100 -o recon_results.txt
```

## 🔮 Future Perspectives (Roadmap)
To elevate this reconnaissance tool further, the following features could be implemented:
1. **API Integration (Passive Recon):** Integrate APIs like `crt.sh` (Certificate Transparency logs) or `SecurityTrails` to find subdomains passively without sending any direct DNS queries to the target.
2. **Wildcard Detection:** Implement a check to detect if a domain uses "Wildcard DNS" (where literally *any* made-up subdomain resolves to a valid IP), which normally breaks dictionary-based enumeration.
