import tkinter as tk
import requests

API_URL = "https://qr-scanner-api-6i39.onrender.com/receive"

def send_qr_data(qr_data): 
    response = requests.post(API_URL, json={"qr": qr_data})  

def on_scan(event):
    qr = entry.get().strip()
    if qr:
        send_qr_data(qr)
    entry.delete(0, tk.END)

# Create hidden tkinter window
root = tk.Tk()
root.title("QR Sender")
root.geometry("200x1")  # Tiny invisible window
root.overrideredirect(True)  # Remove border/title
root.attributes("-topmost", True)  # Stay on top
root.withdraw()  # Hide window

# Add hidden entry field
entry = tk.Entry(root)
entry.bind("<Return>", on_scan)
entry.pack()

entry.focus_force()
root.deiconify()  # Show window (but minimal)
root.mainloop()
