import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Elite X-Name Service</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Montserrat:wght@400&display=swap');
        body { background-color: #111; color: #0f0; font-family: 'Montserrat', sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; text-shadow: 0 0 5px #0f0; }
        .card { background: #1a1a1a; border: 1px solid #0f0; border-radius: 15px; box-shadow: 0 0 20px rgba(0,255,0,0.2); padding: 40px; text-align: center; width: 80%; max-width: 600px; }
        .card h1 { font-family: 'Orbitron', sans-serif; color: #0f0; font-size: 3em; margin: 0; }
        .card p { color: #aaa; }
        .hint { margin-top: 30px; font-size: 1.1em; color: #0a0; max-width: 600px; text-align: center; }
        .hint code { background: #222; padding: 3px 6px; border-radius: 4px; border: 1px solid #0a0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Greetings, {{ name }}!</h1>
        <p>Welcome to the Securinets.</p>
    </div>

    <div class="hint">
        <p>Tired of being a guest? True hackers introduce themselves with an header.</p>
        <p>Try sending a request with it. The template engine is quite... flexible.</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    
    name_from_header = request.headers.get('X-Name', 'Guest')

    template = HTML_TEMPLATE.replace("{{ name }}", name_from_header)
    
    return render_template_string(template)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
