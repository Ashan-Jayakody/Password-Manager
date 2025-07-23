import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_master_password(hashed):
    with open("master.txt", "w") as f:
        f.write(hashed)

def verify_master_password(input_pass) -> bool:
    if not os.path.exists("master.txt"):
        return False
    with open("master.txt", "r") as f:
        saved = f.read()
    return hash_password(input_pass) == saved