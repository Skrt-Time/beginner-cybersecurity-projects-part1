import hashlib
import argparse
import time
import itertools
import string
import sys
from typing import Optional

def hash_string(text: str, algorithm: str) -> str:
    """Hashes a given string using the specified algorithm."""
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(text.encode('utf-8'))
    return hash_obj.hexdigest()

def dictionary_attack(target_hash: str, wordlist_path: str, algorithm: str) -> Optional[str]:
    """Performs a dictionary attack against a given hash."""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_number, word in enumerate(file, 1):
                clean_word = word.strip()
                if hash_string(clean_word, algorithm) == target_hash:
                    print(f"[*] Password found at line {line_number}")
                    return clean_word
        return None
    except FileNotFoundError:
        print(f"[-] Error: Wordlist file '{wordlist_path}' not found.")
        sys.exit(1)

def brute_force_attack(target_hash: str, max_length: int, algorithm: str) -> Optional[str]:
    """Performs a brute-force attack using alphanumeric characters and symbols."""
    # Define the character set (lowercase, uppercase, digits, and punctuation)
    charset = string.ascii_letters + string.digits + string.punctuation
    print(f"[*] Starting Brute-Force attack up to length {max_length}...")
    print(f"[*] Character set size: {len(charset)}")
    
    attempts = 0
    for length in range(1, max_length + 1):
        print(f"[*] Trying all combinations of length {length}...")
        for guess_tuple in itertools.product(charset, repeat=length):
            attempts += 1
            guess = "".join(guess_tuple)
            
            if hash_string(guess, algorithm) == target_hash:
                print(f"[*] Password found after {attempts} attempts.")
                return guess
    return None

def main():
    parser = argparse.ArgumentParser(description="Advanced Password Cracker (Dictionary & Brute-Force)")
    parser.add_argument("-t", "--target", required=True, help="The target hash to crack")
    parser.add_argument("-a", "--algorithm", choices=['md5', 'sha1', 'sha256', 'sha512'], default='md5', help="Hash algorithm (default: md5)")
    
    # Mutually exclusive group: user must choose either dictionary or brute-force
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-w", "--wordlist", help="Path to the wordlist file for dictionary attack")
    group.add_argument("-b", "--bruteforce", type=int, help="Maximum password length for brute-force attack")

    args = parser.parse_args()

    print("="*50)
    print("🔒 Python Password Cracker Tool")
    print("="*50)
    print(f"Target Hash : {args.target}")
    print(f"Algorithm   : {args.algorithm.upper()}")
    
    start_time = time.time()
    result = None

    if args.wordlist:
        print(f"Mode        : Dictionary Attack")
        print(f"Wordlist    : {args.wordlist}\n")
        result = dictionary_attack(args.target, args.wordlist, args.algorithm)
    elif args.bruteforce:
        print(f"Mode        : Brute-Force Attack")
        print(f"Max Length  : {args.bruteforce}\n")
        result = brute_force_attack(args.target, args.bruteforce, args.algorithm)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    print("\n" + "="*50)
    if result:
        print(f"[+] SUCCESS! Password is: {result}")
    else:
        print("[-] FAILED. Password could not be cracked.")
    print(f"[*] Time elapsed: {elapsed_time} seconds.")
    print("="*50)

if __name__ == "__main__":
    main()
