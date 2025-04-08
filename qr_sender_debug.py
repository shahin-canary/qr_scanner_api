import msvcrt
import time

print("🟢 Listening... Start scanning QR codes:")

buffer = ""

while True:
    if msvcrt.kbhit():
        char = msvcrt.getwche()
        if char == "\r":
            print("\n✅ Received:", buffer)
            buffer = ""
        else:
            buffer += char
    time.sleep(0.01)
