from flask import Flask, request, session, render_template
import random
import os

app = Flask(__name__)

# --- THE FIX IS HERE ---
# The secret key MUST be a static, consistent value for sessions to work
# across multiple Gunicorn workers. The previous os.urandom(24) created a
# different key for each worker process, causing session errors.
app.secret_key = "a-super-secret-and-static-key-for-the-ctf"

FLAG = "Securinets{r4c3_c0nd1t10ns_4r3_fun_w1th_scr1pt1ng!}"

@app.route('/')
def home():
    """
    Renders the main page with instructions.
    Initializes a new key in the user's session if one doesn't exist.
    """
    if 'key' not in session:
        session['key'] = random.randint(1, 1000)
        session['getflag'] = False
    return render_template('index.html')

@app.route('/guess')
def guess():
    """
    Handles the user's key guess.
    This is now multiplayer-safe.
    """
    # Ensure the user has a key in their session
    if 'key' not in session:
        return "Please visit the main page first to start the challenge."

    user_input_str = request.args.get('key')
    if user_input_str is None:
        return "Please provide your guess with the 'key' parameter. Example: /guess?key=123"

    try:
        user_guess = int(user_input_str)
    except (ValueError, TypeError):
        return "Invalid key format. It must be an integer."

    # Compare user's guess with the key stored in THEIR session
    if user_guess == session['key']:
        session['getflag'] = True
        return "Correct! The vault is temporarily unlocked. Quick, get the flag!"
    else:
        # If the guess is wrong, reset the key for this user ONLY and deny access.
        session['key'] = random.randint(1, 1000)
        session['getflag'] = False
        return "Incorrect key. The security system has reset the key. Try again."

@app.route('/flag')
def flag():
    """
    Provides the flag only if the user has successfully guessed the key in the same session.
    """
    # Check the 'getflag' status in the user's session
    if session.get('getflag'):
        # Reset the flag status to prevent reuse
        session['getflag'] = False
        session.pop('key', None) # Also remove the key
        return f"Congratulations! Here is your flag: {FLAG}"
    else:
        return "Access Denied. You need to guess the correct key first."