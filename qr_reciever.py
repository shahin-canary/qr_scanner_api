# api_server.py
from flask import Flask, request, render_template_string, jsonify

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
        button { margin-bottom: 15px; padding: 10px 20px; background: #d9534f; color: white; border: none; border-radius: 5px; cursor: pointer; }
        ul { list-style-type: none; padding: 0; }
        li { background: #fff; margin: 5px 0; padding: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: relative; transition: background 0.3s; }
        .delete-btn {
            position: absolute;
            top: 8px;
            right: 10px;
            display: none;
            background: none;
            border: none;
            color: red;
            font-size: 18px;
            cursor: pointer;
        }
        li:hover .delete-btn {
            display: inline;
        }
    </style>
</head>
<body>
    <h2>Received QR Codes</h2>
    <button onclick="clearAll()">Clear All</button>
    <ul id="qrList">
        {% for code in qr_codes %}
            <li data-index="{{ loop.index0 }}">
                {{ code }}
                <button class="delete-btn" onclick="deleteCode({{ loop.index0 }})">&times;</button>
            </li>
        {% else %}
            <li>No QR codes received yet.</li>
        {% endfor %}
    </ul>

    <script>
        function clearAll() {
            fetch('/clear', { method: 'POST' })
                .then(() => location.reload());
        }

        function deleteCode(index) {
            fetch('/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index: index })
            })
            .then(() => location.reload());
        }
    </script>
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

@app.route('/clear', methods=['POST'])
def clear():
    qr_codes.clear()
    return {"status": "cleared"}

@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    index = data.get('index')
    if index is not None and 0 <= index < len(qr_codes):
        removed = qr_codes.pop(index)
        print("QR Data Deleted:", removed)
        return {"status": "deleted"}
    return {"status": "invalid index"}, 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
