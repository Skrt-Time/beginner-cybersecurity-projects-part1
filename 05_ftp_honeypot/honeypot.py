import socket
import threading
import argparse
import logging
import sys
from datetime import datetime

def setup_logger(log_file):
    """Configures the logging format to capture attacker credentials."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - [HONEYPOT] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def handle_client(client_socket, client_address):
    """Handles an individual attacker's connection to the honeypot."""
    ip = client_address[0]
    port = client_address[1]
    print(f"[*] Incoming connection from {ip}:{port}")
    
    try:
        # 1. Send fake FTP Server Banner
        client_socket.send(b"220 (vsFTPd 3.0.3)\r\n")
        username = "Unknown"
        
        # 2. Loop to handle multiple commands (like SYST, OPTS) before the login
        while True:
            data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
            
            if not data:
                break # Attacker disconnected
                
            command = data.upper()
            
            if command.startswith("USER"):
                username = data.split(' ', 1)[1] if ' ' in data else "Unknown"
                client_socket.send(b"331 Please specify the password.\r\n")
                
            elif command.startswith("PASS"):
                password = data.split(' ', 1)[1] if ' ' in data else "Empty"
                
                # Capture and log the credentials!
                logging.info(f"Target: {ip} | USER: {username} | PASS: {password}")
                print(f"[!] CAPTURE: IP={ip} | User='{username}' | Pass='{password}'")
                
                # Simulate an authentication failure and break the loop to disconnect
                client_socket.send(b"530 Login incorrect.\r\n")
                break
                
            elif command.startswith("QUIT"):
                client_socket.send(b"221 Goodbye.\r\n")
                break
                
            else:
                # Tell the FTP client we don't support its extra features (AUTH TLS, SYST, etc.)
                # This forces it to move on to the actual USER/PASS login phase.
                client_socket.send(b"502 Command not implemented.\r\n")
                
    except socket.timeout:
        print(f"[-] Connection timed out for {ip}")
    except Exception as e:
        print(f"[-] Error handling {ip}: {e}")
    finally:
        client_socket.close()

def main():
    parser = argparse.ArgumentParser(description="Interactive FTP Honeypot (Deception Technology)")
    parser.add_argument("-p", "--port", type=int, default=2121, help="Port to listen on (default: 2121 to avoid needing sudo)")
    parser.add_argument("-b", "--bind", default="0.0.0.0", help="IP address to bind to (default: 0.0.0.0 for all interfaces)")
    parser.add_argument("-l", "--log", default="honeypot_captures.log", help="File to save captured credentials")
    
    args = parser.parse_args()
    
    setup_logger(args.log)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((args.bind, args.port))
        server_socket.listen(5)
    except PermissionError:
        print(f"[-] Error: Permission denied. If using a port < 1024, use 'sudo'.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Failed to bind to {args.bind}:{args.port} - {e}")
        sys.exit(1)

    print("="*65)
    print("🍯 Blue Team Interactive FTP Honeypot")
    print("="*65)
    print(f"[*] Listening on  : {args.bind}:{args.port}")
    print(f"[*] Log File      : {args.log}")
    print(f"[*] Status        : ACTIVE. Waiting for attackers...")
    print("="*65)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_socket.settimeout(60) # Increased timeout so you have time to type
            
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[*] Ctrl+C detected. Shutting down the honeypot safely...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
