# 15 - Linux Privilege Escalation Analyzer

A fast, dependency-free Python script designed for local system auditing. This tool mimics the behavior of industry-standard enumeration scripts (like LinPEAS) used during the Privilege Escalation phase of a penetration test or a Capture The Flag (CTF) event.

## 🛡️ What is Privilege Escalation?
When an attacker gains initial access to a Linux machine (e.g., via a compromised web server), they typically land as a low-privileged user (like `www-data`). Their next objective is to find a system misconfiguration that allows them to elevate their permissions to the superuser (`root`). This script automates the hunt for those exact misconfigurations.

## ✨ Technical Features
* **File Permission Auditing:** Analyzes the `st_mode` bitmask using Python's `stat` module to detect if critical authentication files (`/etc/passwd`, `/etc/shadow`) are improperly configured as world-readable or world-writable.
* **SUID Binary Hunting:** Systematically walks through common binary directories (`/bin`, `/usr/bin`, etc.) to locate executables with the `SUID` bit set. SUID binaries run with the permissions of the file owner (usually root) rather than the user executing them, making them prime targets for exploitation (via GTFOBins).
* **Configuration Parsing:** Automatically reads and parses service configurations (like `sshd_config`) to detect dangerous policies such as `PermitRootLogin yes`.

## ⚙️ Prerequisites & Installation

1. **Initialize the environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(No external `pip` requirements are needed. Relies entirely on the Python Standard Library for maximum portability on restricted target machines).*

## 📖 Help Menu
```bash
python privesc_analyzer.py --help
```

## 💻 Command Examples

**1. Basic System Audit:**
Run the analyzer on your current Linux machine to check for basic misconfigurations:
```bash
python privesc_analyzer.py
```

**2. Exporting an Audit Report:**
Run the analyzer and dump the findings and the list of discovered SUID binaries to a text file for further review:
```bash
python privesc_analyzer.py -o security_audit.txt
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool into a comprehensive enumeration suite, the following features are planned:
1. **Cron Job Analysis:** Parse `/etc/crontab` and `/etc/cron.d/` to find scheduled tasks running as root that execute world-writable shell scripts.
2. **Sudo Privileges (`sudo -l`):** Automate the checking of commands the current user is allowed to run via `sudo` without a password.
3. **Exploit Suggestion:** Integrate a local mapping of the `GTFOBins` database to automatically alert the user if a specific discovered SUID binary (like `nmap`, `vim`, or `find`) has a known privilege escalation bypass.
