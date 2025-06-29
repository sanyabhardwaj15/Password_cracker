import argparse
import hashlib
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def check_hash(password, hash_type, target_hash):
    hash_func = getattr(hashlib, hash_type)
    hashed = hash_func(password.encode()).hexdigest()
    return hashed == target_hash, password

def generate_passwords(charset, min_len, max_len):
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(charset, repeat=length):
            yield ''.join(combo)

def crack_hash(target_hash, hash_type, wordlist=None, min_len=1, max_len=4, max_workers=4):
    passwords = []

    if wordlist:
        try:
            with open(wordlist, 'r') as f:
                passwords = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"[!] Wordlist file '{wordlist}' not found.")
            return
    else:
        charset = string.ascii_letters + string.digits
        passwords = generate_passwords(charset, min_len, max_len)

    print(f"[+] Starting hash cracking using {hash_type.upper()}...")
    found = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        if isinstance(passwords, list):
            pbar = tqdm(passwords, desc="Cracking")
            futures = [executor.submit(check_hash, pwd, hash_type, target_hash) for pwd in pbar]
        else:
            total = sum(len(string.ascii_letters + string.digits) ** i for i in range(min_len, max_len + 1))
            pbar = tqdm(passwords, total=total, desc="Cracking")
            futures = [executor.submit(check_hash, pwd, hash_type, target_hash) for pwd in pbar]

        for future in futures:
            result, pwd = future.result()
            if result:
                print(f"\n✅ Password found: {pwd}")
                found = True
                break

    if not found:
        print("\n❌ Password not found. Try a longer wordlist or increase max_length.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🔐 Python Password Cracker Tool")
    parser.add_argument("hash", help="Target hash to crack")
    parser.add_argument("--hash_type", default="md5", help="Hash algorithm (md5, sha1, sha256)")
    parser.add_argument("--wordlist", help="Path to wordlist file")
    parser.add_argument("--min_length", type=int, default=1, help="Minimum password length for brute-force")
    parser.add_argument("--max_length", type=int, default=4, help="Maximum password length for brute-force")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads (default: 4)")
    args = parser.parse_args()

    crack_hash(
        target_hash=args.hash,
        hash_type=args.hash_type.lower(),
        wordlist=args.wordlist,
        min_len=args.min_length,
        max_len=args.max_length,
        max_workers=args.threads
    )
