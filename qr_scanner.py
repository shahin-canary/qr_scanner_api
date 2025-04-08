from flask import Flask, request

app = Flask(__name__)
latest_qr = ""

@app.route('/upload', methods=['POST'])
def upload():
    global latest_qr
    latest_qr = request.json.get('data', '')
    print("Received:", latest_qr)
    return {"status": "success"}

@app.route('/get', methods=['GET'])
def get_qr():
    return {"data": latest_qr}

if __name__ == '__main__':
    app.run(port=5000)
