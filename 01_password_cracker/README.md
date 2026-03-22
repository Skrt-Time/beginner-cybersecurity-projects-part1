# 01 - Advanced Password Cracker

A robust, command-line password cracking tool built in Python. This project demonstrates the vulnerability of weak passwords by employing both **Dictionary** and **Brute-Force** attack vectors against common cryptographic hashes.

## ⚠️ Educational Disclaimer
**This tool was developed strictly for educational purposes and ethical hacking practice.** Do not use this software to attack systems, networks, or accounts that you do not own or do not have explicit written permission to test. The author is not responsible for any misuse or damage caused by this tool.

## ✨ Key Features
* **Multiple Hash Algorithms:** Supports `MD5`, `SHA1`, `SHA256`, and `SHA512`.
* **Dual Attack Modes:** * *Dictionary Attack:* Fast cracking using predefined wordlists.
  * *Brute-Force Attack:* Exhaustive search using combinations of letters, numbers, and symbols.
* **Performance Tracking:** Built-in timer to measure the duration of the cracking process.
* **Clean CLI:** Professional command-line interface built with Python's `argparse`.

## ⚙️ Prerequisites & Installation
This script uses only built-in Python libraries. No external dependencies are required.
* Python 3.6 or higher.

## 📖 Help Menu
You can access the built-in manual at any time by running the following command:
```bash
python cracker.py --help
```

**Output:**
```text
usage: cracker.py [-h] -t TARGET [-a {md5,sha1,sha256,sha512}] (-w WORDLIST | -b BRUTEFORCE)

Advanced Password Cracker (Dictionary & Brute-Force)

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The target hash to crack
  -a {md5,sha1,sha256,sha512}, --algorithm {md5,sha1,sha256,sha512}
                        Hash algorithm (default: md5)
  -w WORDLIST, --wordlist WORDLIST
                        Path to the wordlist file for dictionary attack
  -b BRUTEFORCE, --bruteforce BRUTEFORCE
                        Maximum password length for brute-force attack
```

## 💻 Command Examples

Here are practical examples of how to run the tool.

### Dictionary Attacks

**Crack an MD5 hash using a local wordlist:**
```bash
python cracker.py -t 5d41402abc4b2a76b9719d911017c592 -w wordlist.txt
```

**Crack a SHA-256 hash using the standard Linux dictionary:**
*(Available on most Unix/Linux systems by default)*
```bash
python cracker.py -t 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 -w /usr/share/dict/words -a sha256
```

**Crack a SHA-512 hash using Kali/Parrot OS standard wordlist (RockYou):**
```bash
python cracker.py -t 309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f... -w /usr/share/wordlists/rockyou.txt -a sha512
```

### Brute-Force Attacks

**Brute-force an MD5 hash (Max length of 4 characters):**
```bash
python cracker.py -t 81dc9bdb52d04dc20036dbd8313ed055 -b 4
```

**Brute-force a SHA-1 hash (Max length of 5 characters):**
```bash
python cracker.py -t 8cb2237d0679ca88db6464eac60da96345513964 -b 5 -a sha1
```

## 🔮 Future Perspectives (Roadmap)
To elevate this tool further, the following features could be implemented:
1. **Multiprocessing:** Distribute the brute-force workload across multiple CPU cores to increase attempts per second.
2. **Salt Support:** Add functionality to crack hashes that use cryptographic salts (e.g., `hash(salt + password)`).
3. **GPU Acceleration:** Rewrite the hashing core using PyCUDA to leverage the parallel processing power of modern Graphics Cards.
