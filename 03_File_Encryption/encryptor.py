# 03 - Secure File Encryption Tool

A robust command-line utility built in Python to encrypt and decrypt files using **Symmetric Cryptography**. This tool utilizes the `cryptography` library (specifically the Fernet module, which guarantees that data encrypted using it cannot be manipulated or read without the key, leveraging AES in CBC mode).

## ⚠️ Educational Disclaimer
**This tool is provided for educational purposes to demonstrate cryptographic concepts.** While it uses strong, industry-standard algorithms, managing encryption keys securely is a complex topic. Do not use this script as your sole method of protecting highly classified or life-critical data without a proper Key Management System (KMS).

## ✨ Key Features
* **Key Generation:** Easily generate secure, random symmetric keys.
* **File Encryption:** Encrypt any type of file (text, images, PDFs, etc.) securely.
* **File Decryption:** Restore encrypted files to their original state using the correct key.
* **Integrity Checks:** The underlying Fernet implementation includes a MAC (Message Authentication Code) to ensure the ciphertext has not been tampered with.

## ⚙️ Prerequisites & Installation
This script requires the third-party `cryptography` library.

Install the required Python library using pip:
```bash
pip install cryptography
```

## 📖 Help Menu
This tool uses subcommands (`generate-key`, `encrypt`, `decrypt`). You can access the manual by running the `-h` or `--help` command:

```bash
python encryptor.py --help
```

**Output:**
```text
usage: encryptor.py [-h] {generate-key,encrypt,decrypt} ...

Secure File Encryption/Decryption Tool using AES (Fernet)

positional arguments:
  {generate-key,encrypt,decrypt}
                        Available commands
    generate-key        Generate a new symmetric encryption key
    encrypt             Encrypt a file
    decrypt             Decrypt a file

options:
  -h, --help            show this help message and exit
```
*(You can also use `python encryptor.py encrypt --help` to see options for specific commands).*

## 💻 Command Examples

Here is the typical workflow to secure a file.

### 1. Generate an Encryption Key
First, you need to generate a secure key. Keep this file safe!
```bash
python encryptor.py generate-key -k my_secret.key
```

### 2. Encrypt a File
Use the generated key to encrypt a sensitive document (e.g., `passwords.txt`).
```bash
python encryptor.py encrypt -f passwords.txt -k my_secret.key
```
*This will generate an encrypted file named `passwords.txt.enc`.*

### 3. Decrypt a File
To restore the encrypted file to its original readable format:
```bash
python encryptor.py decrypt -f passwords.txt.enc -k my_secret.key
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features could be implemented:
1. **Asymmetric Cryptography (RSA):** Add support for public/private key pairs to allow secure file sharing between two different users.
2. **Password-Based Key Derivation (PBKDF2):** Instead of saving a key to a file, allow the user to type a password, and mathematically derive the encryption key from that password.
3. **Directory Encryption:** Implement a recursive function to encrypt all files within a specific folder at once.
