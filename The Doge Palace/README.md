# CTF Write-up: The Doge Palace

**Category:** Web Exploitation / Information Disclosure  
**Difficulty:** Easy  
**Goal:** Discover hidden files exposed by server misconfiguration.

## 1. Reconnaissance

### Initial Look
We start by accessing the main page `index.html`. It's a simple page with some ASCII art of a Doge. Inspecting the source code reveals a comment at the bottom:

```html
<!-- ohhhhh crawlers are here !!!!!!!-->
```

This is a clear hint to check the `robots.txt` file, which is used to instruct web crawlers.

### Following the Crumbs
Checking `/robots.txt`:

```text
User-wow-agent: *
Disallow: /very/secrets/
Disallow: /you/dumb/

# much rules.
# many style.
# the next clue is hidden in the pretty colors file.
```

The comments explicitly point us to the "pretty colors file," which refers to the CSS stylesheet.

### CSS Analysis
We navigate to `/css/main-style.css`. Inside, we find another comment block:

```css
/*
   such access control.
   very apache.
   much old config file.
   wow.
*/
```

"Very apache" and "old config file" are references to `.htaccess` files, which are configuration files used by the Apache web server (not Nginx).

## 2. Vulnerability Analysis

The server is actually running Nginx (as seen in the `docker-compose.yml`), not Apache. However, looking at the provided `nginx.conf`, we spot a critical misconfiguration:

```nginx
# This is important! It allows access to dotfiles.
location ~ /\. {
    allow all;
}
```

Normally, web servers block access to "dotfiles" (files starting with `.`), as they often contain sensitive configuration or metadata (like `.git`, `.env`, `.htaccess`). This configuration explicitly allows access to them.

## 3. Exploitation

### Accessing .htaccess
Since we know the server allows dotfiles, and the CSS hinted at an "Apache config," we try to access:

`http://<target-ip>:5009/.htaccess`

The server returns the file content:

```text
# wow such deny from all
# much security
# a mac developer was here... he was very messy.
```

### The "Mac Developer" Artifact
The `.htaccess` file doesn't contain the flag, but it gives us the final clue: "a mac developer was here... he was very messy."

On macOS, the operating system automatically creates hidden metadata files called `.DS_Store` in directories accessed by Finder. These files contain a list of filenames in that directory, including hidden ones.

### Retrieving the Flag
We navigate to `http://<target-ip>:5009/.DS_Store`.
The server downloads the binary file.

We can analyze this file using a tool like `strings` or a specific `.DS_Store` parser (e.g., Python's `ds_store` library).

**Command:** `strings .DS_Store`

The output will reveal a unique filename that isn't visible in the directory listing (e.g., `very_secret_flag.txt`).

Navigate to that file to get the flag.

## Summary

1. **Robots.txt** -> Pointed to CSS.
2. **CSS** -> Pointed to Apache config (`.htaccess`).
3. **Nginx Config** -> Revealed that dotfiles are accessible.
4. **.htaccess** -> Pointed to Mac artifacts (`.DS_Store`).
5. **.DS_Store** -> Leaked the hidden flag filename.
