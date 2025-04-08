# api_server.py
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

qr_codes = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="3">
    <title>QR Data Viewer</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #eef2f3, #8e9eab);
            padding: 40px;
            color: #333;
        }

        h2 {
            margin-bottom: 20px;
            color: #2c3e50;
            text-shadow: 1px 1px 1px #ccc;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        button {
            padding: 12px 25px;
            background-color: #e74c3c;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }

        button:hover {
            background-color: #c0392b; 
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            background-color: #f9f9f9;
            margin: 10px 0;
            padding: 15px 20px;
            border-radius: 12px;
            position: relative;
            box-shadow: 0 4px 10px rgba(0,0,0,0.07); 
        }
 

        .delete-btn {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #e74c3c;
            font-size: 20px;
            display: none;
            cursor: pointer;
        }

        li:hover .delete-btn {
            display: block;
        }

        .no-data {
            font-style: italic;
            color: #666;
        }

        @media screen and (max-width: 600px) {
            body {
                padding: 20px;
            }

            .container {
                padding: 20px;
            }

            button {
                width: 100%;
                font-size: 14px;
            }

            li {
                font-size: 14px;
            }
        }
 
    </style>
</head>
<body>
    <div class="container fade-in">
        <h2>Received QR Codes</h2>
        <button onclick="clearAll()">Clear All</button>
        <ul id="qrList">
            {% for code in qr_codes %}
                <li data-index="{{ loop.index0 }}">
                    {{ code }}
                    <button class="delete-btn" onclick="deleteCode({{ loop.index0 }})">&times;</button>
                </li>
            {% else %}
                <li class="no-data">No QR codes received yet.</li>
            {% endfor %}
        </ul>
    </div>

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
