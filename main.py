from encryption import *
from database import *
from auth import *

def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    key = load_key()
    encrypted_pw = encrypt_password(password,key)

    data = load_passwords()
    data.append({"website":website, "username":username, "password":encrypted_pw})
    save_passwords(data)
    print("Password saved.")

def view_passwords():
    key = load_key()
    for entry in load_passwords():
        try:
            decrypted = decrypt_password(entry["password"], key)
        except:
            decrypted = "[invalid key]"
        print(f"{entry['website']} | {entry['username']} | {decrypted}")


def main():
    if not os.path.exists("secret.key"):
        save_key(generate_key())
        print("Encryption key granted.")

    master = input("Enter master password: ")
    if not os.path.exists("master.txt"):
        save_master_password(hash_password(master))
        print("Master password set.")
    elif not verify_master_password(master):
        print("Wrong password!")
        return
    
    while True:
        print("\n1. Add Password\n2. View passwords\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        else:
            break

if __name__ == "__main__":
    main()
    