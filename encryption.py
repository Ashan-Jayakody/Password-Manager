from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key() # Generates a fresh fernet key

def load_key():
    return open("secret.key","rb").read()

def save_key(key):
    with open("secret.key", "wb") as f:
        f.write(key)

def encrypt_password(password, key):
    return Fernet(key).encrypt(password.encode()).decode()

def decrypt_password(token, key):
    return Fernet(key).decrypt(token.encode()).decode()
