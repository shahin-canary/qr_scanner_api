import threading
import requests
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

API_URL = "https://qr-scanner-api-6i39.onrender.com/receive"

def log_message(msg):
    with open("qr_log.txt", "a") as f:
        f.write(msg + "\n")

def send_qr_data(qr_data):
    try:
        response = requests.post(API_URL, json={"qr": qr_data})
        log_message(f"Sent: {qr_data}")
    except Exception as e:
        log_message(f"Error sending QR: {e}")

def read_qr_input():
    while True:
        try:
            qr_data = input().strip()
            if qr_data:
                send_qr_data(qr_data)
        except Exception as e:
            log_message(f"QR input error: {e}")

def create_image():
    # Create a simple icon image
    image = Image.new('RGB', (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.ellipse((24, 24, 40, 40), fill="white")
    return image

def on_quit(icon, item):
    icon.stop()
    sys.exit(0)

def main():
    threading.Thread(target=read_qr_input, daemon=True).start()

    icon = Icon("QR Sender", icon="tray.ico", menu=Menu(MenuItem("Quit", on_quit)))

    icon.icon = create_image()
    icon.menu = Menu(MenuItem("Quit", on_quit))
    icon.run()

if __name__ == "__main__":
    main()


