# 06 - Universal Log Analyzer (Heuristic Anomaly Detector)

A smart, Blue Team Python utility designed to parse **any standard log file** (SSH, Apache, Nginx, FTP, etc.) to identify and flag potential Brute-Force attacks or unauthorized access attempts. 

Unlike strict parsers that only look for one specific sentence, this tool uses a **Heuristic Approach**. It scans each log entry for common failure keywords (e.g., `fail`, `denied`, `unauthorized`) and automatically extracts the associated IPv4 addresses using Regular Expressions.

## ⚠️ Educational Disclaimer
**This tool is strictly for educational purposes.** It is a monitoring and alerting Proof of Concept to understand how defensive security mechanisms operate across different services. It does not replace enterprise SIEM (Security Information and Event Management) solutions.

## ✨ Key Features
* **Universal Compatibility:** Works out-of-the-box with `auth.log`, Apache `error.log`, `vsftpd.log`, and many custom application logs.
* **Heuristic Detection:** Relies on a flexible list of keywords rather than rigid string matching, making it resilient to log format changes.
* **Custom Thresholds:** Adjust the sensitivity of the detector by defining how many suspicious events are required before an IP is flagged.
* **Frequency Analysis:** Uses Python's `collections.Counter` to quickly aggregate and sort attacker IPs by the volume of their requests.

## ⚙️ Prerequisites & Installation
This script requires **no external dependencies**. It is built entirely using Python's standard library (`re`, `argparse`, `collections`). No `pip` installation or virtual environment is needed.

### 🛡️ Note on Repository Maintenance (.gitignore)
If you export the flagged IPs using the `-o` flag (e.g., `malicious_ips.txt`), ensure these files are ignored by git to keep your repository clean. Add `*.txt` and `*.log` to your `.gitignore`. *A dummy log file (`sample_mixed.log`) is provided for testing without exposing real system logs.*

## 📖 Help Menu
You can access the built-in manual by running the `-h` or `--help` command:

```bash
python log_analyzer.py --help
```

**Output:**
```text
usage: log_analyzer.py [-h] -f FILE [-t THRESHOLD] [-o OUTPUT]

Universal Heuristic Log Analyzer

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the log file
  -t THRESHOLD, --threshold THRESHOLD
                        Number of suspicious events before flagging an IP (default: 3)
  -o OUTPUT, --output OUTPUT
                        Save the list of flagged IPs to a text file
```

## 💻 Command Examples

### 1. Basic Testing (Using the provided mixed log file)
Analyze the dummy file which contains simulated attacks against SSH, Apache, and FTP:
```bash
python log_analyzer.py -f sample.log -t 3
```

### 2. Real-World Usage (Linux)
*Note: Reading the actual system logs usually requires `sudo` privileges.*

**Analyze SSH connections:**
```bash
sudo python log_analyzer.py -f /var/log/auth.log -t 5
```

**Analyze Web Server (Apache) errors:**
```bash
sudo python log_analyzer.py -f /var/log/apache2/error.log -t 10
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features could be implemented:
1. **Machine Learning (AI):** Replace the keyword heuristic with an Isolation Forest or an NLP model (like Word2Vec) to detect behavioral anomalies without any predefined rules.
2. **Auto-Banning (IPS):** Add a module that automatically executes `iptables` or `ufw` commands to block the flagged IPs in real-time.
3. **GeoIP Integration:** Integrate a database (like MaxMind) to display the geographic location (Country/City) of the attacking IPs.
