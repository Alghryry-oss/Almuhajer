import requests
from config import FACEBOOK_ACCESS_TOKEN, INSTAGRAM_ACCESS_TOKEN
from .utils import random_delay

class FacebookCollector:
    BASE = 'https://graph.facebook.com/v18.0'
    
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.params = {'access_token': token}
    
    def get_user(self, user_id):
        url = f"{self.BASE}/{user_id}"
        params = {'fields': 'id,name,username,about,email,link,website,location,birthday,friends.limit(0).summary(true)'}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_posts(self, user_id, limit=100):
        url = f"{self.BASE}/{user_id}/posts"
        params = {'fields': 'id,message,created_time,likes.limit(0).summary(true),comments.limit(0).summary(true)', 'limit': limit}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get('data', [])
    
    # Add more methods: comments, photos, etc.

class InstagramCollector:
    BASE = 'https://graph.instagram.com'
    
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.params = {'access_token': token}
    
    def get_user(self, user_id):
        url = f"{self.BASE}/{user_id}"
        params = {'fields': 'id,username,account_type,media_count'}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_media(self, user_id, limit=50):
        url = f"{self.BASE}/{user_id}/media"
        params = {'fields': 'id,caption,media_type,media_url,timestamp,like_count,comments_count', 'limit': limit}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get('data', [])