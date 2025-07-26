from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set the frontend directory
FRONTEND_DIR = '/home/ubuntu/github_test/objx_platform/frontend'

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Demo response showing this is from GitHub version
        response = f"✅ GITHUB VERSION CONFIRMED! Your message: '{message}' - This is running directly from your GitHub repository with all epic UI features intact!"
        
        return jsonify({
            'success': True,
            'message': response,
            'source': 'GitHub Repository Clone',
            'timestamp': '2025-07-26T15:40:00Z'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Chat error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting OBJX Platform from GitHub Repository...")
    print("📁 Serving files from:", FRONTEND_DIR)
    print("✨ All epic UI features included!")
    app.run(host='0.0.0.0', port=6000, debug=False)

