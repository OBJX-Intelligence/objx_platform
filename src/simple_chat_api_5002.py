#!/usr/bin/env python3
import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import traceback

app = Flask(__name__)
CORS(app)

# Set API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(project_root, 'frontend')

@app.route('/')
def index():
    """Serve the landing page"""
    return send_from_directory(frontend_path, 'index.html')

@app.route('/login.html')
def login():
    """Serve the login page"""
    return send_from_directory(frontend_path, 'login.html')

@app.route('/dashboard_admin.html')
def dashboard_admin():
    """Serve the admin dashboard"""
    return send_from_directory(frontend_path, 'dashboard_admin.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images, etc.)"""
    return send_from_directory(frontend_path, filename)

@app.route('/api/login', methods=['POST'])
def api_login():
    """Demo login endpoint"""
    return jsonify({"status": "success", "redirect": "/dashboard_admin.html"})

@app.route('/api/chat/message', methods=['POST'])
def chat():
    try:
        print("Chat endpoint called")
        data = request.get_json()
        print(f"Received data: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400
        
        message = data.get('message', '')
        print(f"Message: {message}")
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # Create OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        print("OpenAI client created")
        
        # Make API call
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You are an intelligent assistant for the OBJX Intelligence Platform. You help with project management and provide strategic insights. Be helpful and professional.'},
                {'role': 'user', 'content': message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        print("OpenAI response received")
        
        return jsonify({
            'success': True,
            'message': response.choices[0].message.content,
            'provider': 'openai'
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting OBJX Chat API...")
    app.run(host='0.0.0.0', port=5002, debug=True)
