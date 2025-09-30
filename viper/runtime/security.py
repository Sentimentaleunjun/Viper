import hashlib

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()
