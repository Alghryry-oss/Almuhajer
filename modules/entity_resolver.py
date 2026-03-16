from collections import defaultdict
import re

class EntityResolver:
    def __init__(self):
        self.entities = {}  # id -> attributes
        self.relations = []  # (src, tgt, type)
    
    def add_entity(self, entity_id, platform, data):
        self.entities[entity_id] = {
            'platform': platform,
            'username': data.get('username'),
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': self.extract_phone(data.get('bio', '')),
            'profile_url': data.get('link'),
            'raw': data
        }
    
    def extract_phone(self, text):
        if not text:
            return None
        # Simple regex for demonstration
        phones = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        return phones[0] if phones else None
    
    def resolve(self):
        # Link by email
        email_to_ids = defaultdict(set)
        for eid, attrs in self.entities.items():
            if attrs.get('email'):
                email_to_ids[attrs['email']].add(eid)
        for email, ids in email_to_ids.items():
            ids = list(ids)
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):
                    self.relations.append((ids[i], ids[j], 'same_email'))
        
        # Link by phone
        phone_to_ids = defaultdict(set)
        for eid, attrs in self.entities.items():
            if attrs.get('phone'):
                phone_to_ids[attrs['phone']].add(eid)
        for phone, ids in phone_to_ids.items():
            ids = list(ids)
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):
                    self.relations.append((ids[i], ids[j], 'same_phone'))