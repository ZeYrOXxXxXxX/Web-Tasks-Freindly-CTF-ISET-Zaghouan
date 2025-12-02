import jwt
import logging
import threading
import time
from functools import wraps
# Import 'send_from_directory' and 'render_template_string'
from flask import Flask, render_template, request, make_response, redirect, url_for, g, send_from_directory, render_template_string

app = Flask(__name__)

# --- VULNERABILITY 1: Weak Secret Key ---
app.config['SECRET_KEY'] = 'secretkey'
app.config['FLAG'] = 'Securinets{the next hint to get L3ALAM}'

# Logging configuration
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# --- Background task: clear logs every 5 minutes ---
_log_clearer_started = False

def _start_log_clearer():
    global _log_clearer_started
    if _log_clearer_started:
        return
    _log_clearer_started = True

    def _worker():
        # initial delay so logs persist briefly after container start
        time.sleep(300)
        while True:
            try:
                # Truncate the access log in place
                with open('access.log', 'w') as f:
                    f.truncate(0)
                # Also add a marker so admins know it rotated
                logging.info("[system] access.log rotated by scheduler (5m)")
            except Exception:
                # Ignore errors; try again on next cycle
                pass
            time.sleep(150)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

# --- Dummy user database ---
USERS = {
    "guest": "WelcomeToChronoBank123!",
    "admin": "ThisPasswordIsSuperSecureAndCannotBeGuessed" 
}

# --- Wrapper for token verification ---
def token_required(role="any"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.cookies.get('session_token')
            if not token:
                return redirect(url_for('login'))
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                g.user = data.get('user')
                g.role = data.get('role')
                if role != "any" and g.role != role:
                    return "<h1>Access Denied: Insufficient privileges</h1>", 403
            except:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Log every request ---
# Simple blacklist to push players toward obfuscated/encoded payloads via SSTI in User-Agent
BLACKLIST = [
    '__',       # dunder
    '[',        # bracket-notation open
    ']'         # bracket-notation close
]

@app.before_request
def log_request_info():
    # Ensure the log clearer is running (idempotent)
    _start_log_clearer()
    # We log the User-Agent for every request; if it contains banned words, replace it
    ua = request.headers.get('User-Agent', '')
    ua_lc = ua.lower()
    if any(word in ua_lc for word in BLACKLIST):
        ua_to_log = 'you mad hacker'
    else:
        ua_to_log = ua
    logging.info(f"IP: {request.remote_addr}, Path: {request.path}, User-Agent: {ua_to_log}")

# --- Public routes ---
@app.route('/robots.txt')
def serve_robots():
    # Assumes robots.txt is in the 'static' folder
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/internal_memos/<path:filename>')
def serve_memos(filename):
    return send_from_directory('internal_memos', filename)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if USERS.get(username) == password and username == 'guest':
            token = jwt.encode(
                {'user': 'guest', 'role': 'user'},
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('session_token', token)
            return resp
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('session_token', '', expires=0)
    return resp

# --- Protected routes ---
@app.route('/dashboard')
@token_required()
def dashboard():
    if g.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return render_template('dashboard.html', user=g.user)

@app.route('/admin/dashboard')
@token_required(role="admin")
def admin_dashboard():
    return render_template('admin_dashboard.html', user=g.user)

# --- CORRECTED AND MORE ROBUST VULNERABLE LOGS ROUTE ---
@app.route('/admin/logs')
@token_required(role="admin")
def admin_logs():
    try:
        with open('access.log', 'r') as f:
            log_lines = f.readlines()
        
        # Process each line individually to prevent one bad payload from breaking the page
        processed_lines = []
        for line in log_lines:
            try:
                # Wrap the line in a Jinja block so 'self' is defined during rendering,
                # and expose 'os' to the template context for reliability.
                payload_tpl = "{% block b %}" + line.strip() + "{% endblock %}"
                processed_lines.append(render_template_string(payload_tpl, os=__import__('os')))
            except Exception:
                # If a line fails to render (e.g., malformed Jinja), just show the raw line
                processed_lines.append(line.strip())
        
        # Join the processed lines back together with HTML line breaks for display
        logs_content = "<br>".join(processed_lines)
        
        # Now, render the final page with the processed content. Pass logs_content
        # as a variable to avoid a second Jinja evaluation pass on raw lines.
        template = """
        {% extends "base.html" %}
        {% block title %}Logs - ChronoBank{% endblock %}
        {% block content %}
        <div class="container"> 
            <h1>Server Access Logs</h1>
            <div class="logs-box">
                <pre><code>{% autoescape false %}{{ logs_content | safe }}{% endautoescape %}</code></pre>
            </div>
        </div>
        {% endblock %}
        """
        return render_template_string(template, logs_content=logs_content)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=False)

