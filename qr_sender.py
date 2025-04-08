# import requests

# # The scanned QR code
# qr_data = "HelloFromSystemA-123"  # Replace this with actual scanned data

# # Render API URL (System B)
# url = "https://qr-scanner-api-6i39.onrender.com/receive"

# # Send the data
# response = requests.post(url, json={"qr": qr_data})

# # Show result
# print("Response:", response.text)


# import requests

# print("Scan QR code...")

# # Wait for scanner input
# qr_data = input("Scanned QR: ")

# # Send to System B
# url = "https://qr-scanner-api-6i39.onrender.com/receive"
# response = requests.post(url, json={"qr": qr_data})
# print("Response:", response.text)




# qr_sender.pyw
import requests
import time
import sys

API_URL = "https://qr-scanner-api-6i39.onrender.com/receive"

def send_qr_data(qr_data):
    try:
        response = requests.post(API_URL, json={"qr": qr_data})
        print("Sent:", qr_data, "→", response.text)
    except Exception as e:
        print("Error:", e)

def main():
    import msvcrt  # Windows only
    buffer = ""
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getwche()
            if char == "\r":  # Enter key
                qr = buffer.strip()
                if qr:
                    send_qr_data(qr)
                buffer = ""
            else:
                buffer += char
        time.sleep(0.01)

if __name__ == "__main__":
    main()


