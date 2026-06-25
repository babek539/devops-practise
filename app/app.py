from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <h1>🐳 DevOps Practice App</h1>
    <p><strong>Host:</strong> {os.uname().nodename}</p>
    <p><strong>Container IP:</strong> {socket.gethostbyname(socket.gethostname())}</p>
    <p><strong>Status:</strong> ✅ Docker Compose ilə işləyir!</p>
    """

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
