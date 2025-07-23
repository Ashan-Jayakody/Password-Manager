import json

def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            return json.load(f)
    except:
        return []
    
def save_passwords(data):
    with open("passwords.json", "w") as f:
        json.dump(data, f, indent=4)