# Beginner Cybersecurity Projects

Welcome to the **Beginner Cybersecurity Projects** repository. This collection of 15 hands-on, Python-based tools is designed for students, junior analysts, and cybersecurity enthusiasts who want to bridge the gap between theoretical knowledge and practical application.

## About This Repository

While the cybersecurity industry is filled with incredible, robust tools (like Nmap, Gobuster, or Burp Suite), running automated tools without understanding their underlying mechanics limits your growth. 

This repository serves as a **learning laboratory**. By building lightweight alternatives to these mainstream tools, you will gain a deep, under-the-hood understanding of how network protocols operate, how vulnerabilities are exploited, and how defensive mechanisms analyze threats.

These projects cover a wide spectrum of cybersecurity domains, including Open Source Intelligence (OSINT), Penetration Testing (Red Team), Security Operations (Blue Team), and Applied Cryptography.

## Project Directory

The repository is structured into 15 standalone projects, incrementally increasing in complexity:

### Fundamentals & Blue Team (Defense)
* **01 - File Integrity Monitor:** Understanding hashing algorithms and file tampering detection.
* **02 - Basic Network Sniffer:** Capturing and analyzing raw packet data.
* **03 - SSH Brute-Force Detector:** Parsing authentication logs to detect attack patterns.
* **04 - Keylogger Simulation:** Understanding endpoint monitoring and malware behavior.
* **05 - Interactive FTP Honeypot:** Deploying deception technology to capture threat intelligence.
* **06 - ARP Spoofing Detector:** Monitoring local networks for Man-in-the-Middle (MitM) attacks.
* **07 - Offline Malware Analysis:** Utilizing YARA rules and ClamAV in air-gapped environments.

### Reconnaissance & OSINT
* **08 - OSINT Subdomain Enumerator:** Performing multithreaded DNS resolution for attack surface mapping.
* **09 - OSINT Image Metadata Extractor:** Analyzing HEIC/JPG EXIF data and GPS coordinates.
* **10 - Advanced OSINT Web Crawler:** Spidering websites to harvest emails and map hidden infrastructure.

### Applied Cryptography & Forensics
* **11 - Data Smuggler (LSB Steganography):** Hiding covert data payloads inside image pixels.
* **12 - Educational Ransomware Simulator:** Understanding symmetric AES encryption and file locking mechanisms.

### Red Team (Offense) & Web Exploitation
* **13 - Phishing Domain Generator & Verifier:** Automating typosquatting generation and algorithmic brand protection.
* **14 - Advanced Web Vulnerability Scanner:** Building a mini-DAST to detect SQLi, XSS, OS Command Injection, CRLF, and CSRF.
* **15 - Linux Privilege Escalation Analyzer:** Automating local system enumeration (SUID binaries, misconfigurations).

## Getting Started

Each project is contained within its own directory and includes a dedicated `README.md` file. 
To get started with any tool:
1. Navigate to the specific project folder.
2. Read the local `README.md` for technical explanations and OPSEC warnings.
3. Install the specific requirements (it is highly recommended to use a Python virtual environment).
4. Run the script using the provided command examples.

## Going Further (Future Perspectives)

These scripts are built to be robust, yet foundational. At the end of every project's `README.md`, you will find a **"Future Perspectives (Roadmap)"** section. 

If you want to improve your programming and security skills, you are strongly encouraged to use these roadmaps as homework. Try implementing those advanced features yourself to turn these basic scripts into enterprise-grade utilities.

## Contributing and Support

This repository is an open, collaborative learning environment. 

* **Encountered a bug?** If a script crashes, fails to parse a specific input, or contains outdated dependencies, please [Open an Issue](../../issues). Provide the error traceback and the steps to reproduce it.
* **Want to contribute?** We highly encourage pull requests (PRs). If you have completed a feature from the "Future Perspectives" roadmap, optimized the code, or want to add a completely new project to the list, feel free to fork the repository and submit a PR.

## Disclaimer

All tools and scripts in this repository are provided strictly for **educational purposes and authorized ethical hacking**. Never utilize these tools against systems, networks, or applications you do not own or do not have explicit written permission to test.
