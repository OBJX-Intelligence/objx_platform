from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

if __name__ == '__main__':
    print("🚀 OBJX Scaling Test Server")
    print("============================================================")
    print("🌐 Starting server on http://localhost:8000")
    print("📊 Test scaling and interactive elements")
    print("============================================================")
    app.run(host='0.0.0.0', port=8000, debug=True)

