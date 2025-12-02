# CTF Challenge: ChronoBank - The Internal Audit

**Category:** Web  
**Difficulty:** Medium

## Challenge Description

Welcome to ChronoBank, our "impenetrable" online banking application. After a recent security incident, we've tightened our defenses. However, we need you to conduct a new internal audit to ensure no vulnerabilities were missed.

Your mission is to start with low-level guest access and find a way to escalate your privileges to become an administrator. Once you have admin access, you must find a way to read sensitive information from the server environment to prove total compromise.

The flag is stored as an environment variable on the server. Good luck, auditor.

## Setup and Deployment

This challenge is containerized using Docker and Docker Compose for easy setup.

### Requirements
- Docker
- Docker Compose

### Running the Challenge
1. Clone or download all the challenge files into a single directory.
2. Make sure the `access.log` file exists in the root of the directory (it can be empty).
3. From the root of the challenge directory, run the following command:
   ```bash
   docker-compose up --build
   ```
4. The challenge will be accessible at `http://localhost:8080`.

### Stopping the Challenge
To stop and remove the container, run:
```bash
docker-compose down
```

## Intended Solution Path (Spoilers!)

> [!NOTE]
> This section is for the CTF organizer.

The challenge involves three main steps:

### 1. Reconnaissance & Initial Access
- The player starts by checking `robots.txt`, which disallows `/internal_memos/`.
- By visiting this directory, they find `guest_credentials.txt` containing credentials for the guest user.

### 2. Privilege Escalation via JWT Cracking
- Upon logging in as guest, the player receives a JWT session token.
- The token is signed with the HS256 algorithm, but the secret key is very weak (`secretkey`).
- The player must use a tool like hashcat or John the Ripper with a common wordlist (like `rockyou.txt`) to crack the secret.
- Once the secret is found, the player can forge a new JWT with the payload `{"user": "admin", "role": "admin"}` and sign it with the cracked key.
- By replacing their session cookie with the forged admin token, they gain access to the admin panel.

### 3. Log Poisoning SSTI to RCE
- In the admin panel, there is a page to view server access logs (`/admin/logs`).
- The application logs every request's `User-Agent` header.
- The log viewer is vulnerable to a Server-Side Template Injection (SSTI) because it renders the content of the log file directly as a template string.
- The player must use a tool like `curl` to send a request to any page on the server, but with a malicious `User-Agent` header containing an SSTI payload.

**Payload:**
```python
User-Agent: {{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('env')|attr('read')()}}
```

- After sending the payload, the player navigates to the `/admin/logs` page in their browser. The server renders the log file, executes the payload, and the flag is displayed on the page.
