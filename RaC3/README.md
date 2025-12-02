# CTF Challenge: RaC3 (The Race Against Time)

**Category:** Web Exploitation / Scripting  
**Difficulty:** Medium  
**Goal:** Guess the correct key (1-1000) to unlock the vault and retrieve the flag.

## 1. Reconnaissance & Code Analysis

We start by analyzing the source code provided in the `docker-compose.zip` file to understand the application logic.

### The Web Application (`app.py`)
The application is built with Flask. Here are the critical endpoints:

**Initialization (`/`):**
When a user visits the homepage, a random key between 1 and 1000 is generated and stored in the user's session cookie.

```python
if 'key' not in session:
    session['key'] = random.randint(1, 1000) #
```

**The Guess Mechanism (`/guess`):**
The user submits a key.
- **If Correct:** The session variable `getflag` is set to `True`.
- **If Incorrect:** The system resets the key to a new random number immediately.

```python
if user_guess == session['key']:
    session['getflag'] = True
    return "Correct! ..."
else:
    session['key'] = random.randint(1, 1000) #
    session['getflag'] = False
```

**The Flag (`/flag`):**
If `getflag` is `True` in the session, the flag is returned.

### The Vulnerability
At first glance, this looks like a standard brute-force challenge. However, there is a catch: **The target moves.** Every time you guess incorrectly, the lock changes its key.

Since the range is small (1-1000), the probability of guessing correctly on any single request is $1/1000$. By automating this process rapidly, we can force a statistical collision. The challenge name "Race Against Time" and the flag content imply a race condition, but technically, this is a high-frequency brute force against a volatile state.

## 2. The Exploitation Strategy

To solve this, we need a script that:
1. Maintains a persistent session (cookies) so the server tracks us as a single user.
2. Rapidly fires guesses.
3. Checks for the flag immediately upon a successful guess.

The provided `solver.py` implements this using multithreading.

### Analyzing the Solver (`solver.py`)
The solver iterates through numbers 1 to 1000. For each number, it spawns two threads:
- **Guess Thread:** Sends `GET /guess?key=N`.
- **Flag Thread:** Sends `GET /flag`.

```python
# Create the two threads. One for guessing, one for getting the flag.
guess_thread = threading.Thread(target=make_request, args=(s, guess_url, responses, 'guess'))
flag_thread = threading.Thread(target=make_request, args=(s, flag_url, responses, 'flag')) #
```

**Why this works:**
Even though the key resets on failure, we are essentially rolling a 1000-sided die repeatedly.
1. We send a guess (e.g., "50").
2. The server checks if the current random key is "50".
3. If it isn't, the server picks a new random key.
4. We send the next guess (e.g., "51").
5. Eventually, `random.randint(1, 1000)` will coincidentally match our current loop index `i`.
6. When that collision happens, the `guess_thread` sets the session to "unlocked," and the `flag_thread` (or the next iteration) retrieves the flag.

## 3. Execution & Flag

Running the solver script against the Docker container:

1. **Setup:** Ensure the container is running on port 5006 (mapped to internal 5000).
2. **Update Script:** Modify `solver.py` `BASE_URL` to `http://localhost:5006`.
3. **Run:** `python solver.py`

**Console Output:**
The script will rapidly iterate through keys. Eventually, a match occurs:

```text
[*] Trying key: 342
...
[+] SUCCESS! The key was: 342
[+] Flag Response: Congratulations! Here is your flag: Securinets{r4c3_c0nd1t10ns_4r3_fun_w1th_scr1pt1ng!}
```

**The Flag:**
`Securinets{r4c3_c0nd1t10ns_4r3_fun_w1th_scr1pt1ng!}`
