# 05 - Interactive FTP Honeypot (Deception Technology)

A custom-built, Python-based honeypot designed to emulate a vulnerable `vsFTPd` server. This tool falls under the **Blue Team / Cyber Defense** umbrella and is used to gather **Cyber Threat Intelligence (CTI)**. 

By exposing a fake, monitored service to the internet (or an internal network), security analysts can silently capture the IP addresses, usernames, and passwords used by malicious actors and automated botnets during brute-force attacks.

## ⚠️ Educational Disclaimer
**This tool is designed for educational purposes and internal network defense.** Do not deploy honeypots on public infrastructure without properly isolating them (using strict VLANs or dedicated VPS instances) to ensure attackers cannot pivot from the honeypot to your production network.

## ✨ Key Features
* **Active Deception:** Spoofs a realistic FTP banner (`vsFTPd 3.0.3`) to trick automated scanners like Nmap or Masscan into believing it is a legitimate file server.
* **Credential Harvesting:** Interacts with the attacker's client to capture `USER` and `PASS` commands before artificially rejecting the login.
* **Multithreaded Handling:** Uses Python's `threading` module to handle multiple concurrent attackers without freezing the main listener.
* **Silent Logging:** Saves all collected Indicators of Compromise (IoCs) with precise timestamps into a `.log` file for later analysis.

## ⚙️ Prerequisites & Installation
This script is incredibly lightweight and relies entirely on **Python's built-in standard library** (`socket`, `threading`, `logging`). No external `pip` packages or virtual environments are required.

### 🛡️ Note on Repository Maintenance (.gitignore)
To prevent accidentally committing real attacker IP addresses and passwords to GitHub, ensure your `.gitignore` contains the following rule to ignore log files:
```text
*.log
```

## 📖 Help Menu
You can access the built-in manual by running the `-h` or `--help` command:

```bash
python honeypot.py --help
```

## 💻 Command Examples

### 1. Running the Honeypot locally (Unprivileged Port)
By default, the script listens on port `2121`. This is ideal for testing as it does not require `sudo` privileges.
```bash
python honeypot.py
```

### 2. Testing the Honeypot
Open a *second* terminal window and simulate an attacker connecting to your fake server using the native `ftp` client:
```bash
ftp 127.0.0.1 2121
```
*Type any random username and password when prompted. Check your first terminal to see the trap springing in real-time!*

### 3. Production Deployment (Requires Sudo)
To map the honeypot to the standard FTP port (21), you must run the script with root privileges:
```bash
sudo python honeypot.py -p 21 -l attacker_creds.log
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features could be implemented:
1. **Multi-Protocol Support:** Add modular support for fake Telnet (Port 23) and SSH (Port 22, via `paramiko`) listeners.
2. **Discord/Slack Webhooks:** Integrate an alerting system that sends a real-time message to a SOC chat room the second credentials are captured.
3. **Fail2Ban Integration:** Automatically parse the captured IP addresses and write them to an `iptables` blocklist to actively defend the rest of the network from the attacker.
