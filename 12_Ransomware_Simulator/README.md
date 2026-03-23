# 12 - Educational Ransomware Simulator

An applied cryptography project designed to simulate the behavior of a basic Ransomware (CryptoLocker) attack. This tool demonstrates how Advanced Encryption Standard (AES) algorithms can be weaponized to traverse directories, encrypt user data, and append custom extensions (`.locked`), while also providing the mechanism to reverse the damage using the corresponding symmetric key.

## ⚠️ Educational Disclaimer & Safety
**This software is highly destructive by design. It is provided strictly for educational purposes, malware analysis training, and Incident Response (Blue Team) preparation.** To prevent catastrophic accidental damage to the host operating system, this script includes a hardcoded interactive confirmation prompt (Safety Guardrail) that requires the user to manually type a specific keyword before the encryption loop can begin.

## 🛠️ How it Works (The Cryptography)
This tool utilizes **Symmetric Cryptography**, meaning the exact same key is used to both encrypt and decrypt the data. 

It leverages the Python `cryptography` library's `Fernet` implementation. Fernet guarantees that a message encrypted using it cannot be manipulated or read without the key. Under the hood, it uses **AES-128 in CBC mode** (Cipher Block Chaining) for encryption, combined with a **SHA256 HMAC** (Hash-Based Message Authentication Code) to verify data integrity and prevent tampering.

## ✨ Technical Features
* **Key Generation:** Generates a secure, url-safe base64-encoded 32-byte key.
* **Recursive Traversal:** Uses `os.walk` to systematically hunt down files across deep directory trees.
* **Data Overwrite & Deletion:** Securely writes the encrypted data to a new file and actively deletes the original plaintext file from the disk.
* **Incident Simulation:** Automatically drops a `README_RECOVER_FILES.txt` ransom note in the root of the targeted directory upon successful encryption.

## ⚙️ Prerequisites & Installation

1. **Initialize the environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 🛡️ Note on Repository Maintenance (.gitignore)
A `.gitignore` file is included to prevent the accidental upload of `secret.key` files or the `test_target/` directory to public repositories.

## 📖 Help Menu
```bash
python ransomware.py --help
python ransomware.py encrypt --help
```

## 💻 Command Examples (Safe Testing Scenario)

**1. Setup a safe test environment:**
Create a dummy folder with some fake text files to test the script safely.
```bash
mkdir test_target
echo "Confidential bank details" > test_target/bank.txt
echo "Secret passwords" > test_target/passwords.txt
```

**2. Generate the Encryption Key:**
```bash
python ransomware.py keygen -k secret.key
```

**3. Execute the Ransomware (Encryption):**
Target the dummy folder. You will be prompted to type `DESTROY` to confirm.
```bash
python ransomware.py encrypt -d test_target -k secret.key
```
*(Check the `test_target` folder: your files are now unreadable and end with `.locked`, and a ransom note has appeared!)*

**4. Perform Incident Response (Decryption):**
Use the key to unlock the files and restore the folder to its original state.
```bash
python ransomware.py decrypt -d test_target -k secret.key
```

## 🔮 Future Perspectives (Roadmap)
To elevate this simulator into a more advanced Red Team tool, the following features could be explored:
1. **Asymmetric Cryptography (RSA):** Replace the symmetric AES key with a public RSA key hardcoded into the script. The script encrypts the files using the public key, meaning only the attacker (who holds the private key off-site) can generate the decryption tool. This is how modern real-world ransomware operates.
2. **File Signature Evasion:** Obfuscate the Python code or compile it into a `.exe` / `.elf` binary using tools like `PyInstaller` or `Nuitka` to test endpoint EDR/Antivirus detection rates.
3. **Network Persistence:** Add a module that automatically discovers and encrypts mounted network shares (SMB/NFS) to simulate lateral movement.
