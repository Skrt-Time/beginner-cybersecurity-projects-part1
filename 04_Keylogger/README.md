# 04 - Educational Keylogger (Hardware-Level PoC)

A robust, Python-based keystroke logging tool built using the `keyboard` library. Unlike standard user-space loggers that are often blocked by modern Linux display servers (like Wayland), this **Proof of Concept (PoC)** hooks directly into the kernel's hardware input events (`/dev/input/`), demonstrating how advanced rootkits and spyware bypass OS-level protections.

## 🛑 STRICT EDUCATIONAL DISCLAIMER
**This software is provided 100% for educational purposes and ethical security research.** Deploying a keylogger on a computer or network without the explicit, informed consent of the owner and users is a severe violation of privacy and is **illegal** in most jurisdictions. The author assumes absolutely no responsibility for any misuse of this code. 

## ✨ Key Features
* **Hardware-Level Hooking:** Reads directly from kernel input files, bypassing desktop environment restrictions.
* **Live Terminal Echo:** Displays captured keystrokes in real-time in the console for immediate verification.
* **Instant Disk Flush:** Bypasses memory buffers to force write each keystroke to the disk instantly (`os.fsync`), ensuring 0% data loss upon termination.
* **Custom Output:** Allows the user to specify the name and location of the log file via the command line.

## ⚙️ Prerequisites & Installation

This script requires the third-party `keyboard` library. 

**Note for Linux Users:** Because this script reads directly from hardware components, **it requires `root` (sudo) privileges to run.** It is recommended to run this inside an isolated Virtual Environment.

### Step-by-Step Installation:

1. **Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install the dependencies:**
```bash
pip install -r requirements.txt
```

### 🛡️ Note on Repository Maintenance (.gitignore)
To keep your repository clean, ensure your `.gitignore` contains the following to ignore virtual environments and log files:
```text
.venv/
__pycache__/
*.pyc
*.txt
```

## 📖 Help Menu
```bash
sudo .venv/bin/python keylogger.py --help
```

## 💻 Command Examples

### 1. Basic Usage (Requires Sudo)
Because you are using a virtual environment, you must point `sudo` to the virtual environment's Python executable:
```bash
sudo .venv/bin/python keylogger.py
```

### 2. Custom Output File
```bash
sudo .venv/bin/python keylogger.py -o stealth_logs.txt
```

## 🔮 Future Perspectives (Roadmap)
To elevate this educational tool further, the following features could be implemented:
1. **Network Exfiltration:** Add a secure, encrypted socket mechanism to silently transmit the captured keystrokes to a remote listening server instead of saving them to a local file.
2. **Process Hiding:** Research Linux rootkit techniques to hide the keylogger process from commands like `ps` or `top`.
3. **Application Context:** Integrate X11/Wayland window tracking to log not just the keystrokes, but the name of the active application (e.g., "Firefox - Gmail").
