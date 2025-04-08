import tkinter as tk
import requests

API_URL = "https://qr-scanner-api-6i39.onrender.com/receive"

def send_qr_data(qr_data): 
    try:
        response = requests.post(API_URL, json={"qr": qr_data})
        print("✅ Sent:", qr_data, "→", response.text)
    except Exception as e:
        print("❌ Error:", e)

def on_scan(event):
    qr = entry.get().strip()
    if qr:
        send_qr_data(qr)
    entry.delete(0, tk.END)
    entry.focus_force()  # Re-focus after sending

# --- GUI Setup ---
root = tk.Tk()
root.title("QR Sender")
root.geometry("200x20")  # Tiny height (can go smaller)
root.overrideredirect(True)  # No window border
root.attributes("-topmost", True)  # Stay on top
root.configure(bg="black")

entry = tk.Entry(root, font=("Arial", 10))
entry.bind("<Return>", on_scan)
entry.pack(fill=tk.BOTH, expand=True)
entry.focus_force()

def keep_focus():
    # Ensure entry stays focused
    entry.focus_force()
    root.after(500, keep_focus)

keep_focus()
root.mainloop()
