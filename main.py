import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
from encryption import *
from database import *
from auth import *

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x300")

        # Check Master Password
        if not os.path.exists("secret.key"):
            save_key(generate_key())

        self.key = load_key()
        self.check_master()

        # UI components
        self.website_entry = tk.Entry(root, width = 30)
        self.username_entry = tk.Entry(root, width=30)
        self.password_entry = tk.Entry(root, width=30)
        self.delete_entry = tk.Entry(root, width=30)

        tk.Label(root, text="Website").pack()
        self.website_entry.pack()
        tk.Label(root, text="Username").pack()
        self.username_entry.pack()
        tk.Label(root, text="Password").pack()
        self.password_entry.pack()
       
        tk.Button(root, text="Add Password", command=self.add_password).pack(pady=5)
        tk.Button(root, text="View Passwords", command=self.view_passwords).pack(pady=5)
      

        self.tree = ttk.Treeview(root, columns=("Website", "Username", "Password"))
        self.tree.heading("Website", text="Website")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.column("Website", width=120)
        self.tree.column("Username", width=120)
        self.tree.column("Password", width=120)
        self.tree.pack(pady=10)

    def check_master(self):
        master = simpledialog.askstring("Master Password", "Enter master password:", show="*")

        if not os.path.exists("master.txt"):
            save_master_password(hash_password(master))
            messagebox.showinfo("setup", "Master password set.")
        elif not verify_master_password(master):
            messagebox.showerror("Error", "Wrong password. Exiting.")
            self.root.destroy()

    def add_password(self):
         website = self.website_entry.get()
         username = self.username_entry.get()
         password = self.password_entry.get()

         if not website or not username or not password:
             messagebox.showwarning("Missing Info", "Fill all fields")
             return
         
         encrypted_pw = encrypt_password(password, self.key)
         data = load_passwords()
         data.append({"website": website, "username": username, "password": encrypted_pw})
         save_passwords(data)
         messagebox.showinfo("Success", "Password saved.")

         self.website_entry.delete(0, tk.END)
         self.username_entry.delete(0, tk.END)
         self.password_entry.delete(0, tk.END)
       


    def view_passwords(self):
        self.tree.delete(*self.tree.get_children())  # Clear previous rows

        data = load_passwords()
        if not data:
            messagebox.showinfo("Saved Passwords", "No passwords saved yet.")
            return

        for entry in data:
            try:
                decrypted = decrypt_password(entry["password"], self.key)
            except:
                decrypted = "[Error decrypting]"
            self.tree.insert("", "end", values=(entry["website"], entry["username"], decrypted))




if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
    