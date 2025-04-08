# api_server.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Store QR codes in memory
qr_codes = []

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>QR Data Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }
        h2 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { background: #fff; margin: 5px 0; padding: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h2>Received QR Codes</h2>
    <ul>
        {% for code in qr_codes %}
            <li>{{ code }}</li>
        {% else %}
            <li>No QR codes received yet.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, qr_codes=qr_codes)

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    qr_value = data.get('qr')
    if qr_value:
        qr_codes.append(qr_value)
        print("QR Data Received:", qr_value)
    return {"status": "success"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
