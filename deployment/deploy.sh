#!/bin/bash

# OBJX Intelligence Platform - Deployment Script
# Author: Manus AI
# Date: July 25, 2025
# Version: 1.0 - Production Ready

set -e

echo "🚀 OBJX Intelligence Platform - Deployment Script"
echo "=================================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root for security reasons"
   exit 1
fi

# Create deployment directory
DEPLOY_DIR="objx_intelligence_platform"
echo "📁 Creating deployment directory: $DEPLOY_DIR"
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
if [ -f "../requirements_deployment.txt" ]; then
    pip install -r ../requirements_deployment.txt
else
    echo "❌ requirements_deployment.txt not found"
    exit 1
fi

# Copy application files
echo "📋 Copying application files..."
cp ../objx_deployment_app.py app.py
cp ../dashboard_admin.html .
cp ../dashboard_staff.html .
cp ../dashboard_tier3.html .
cp ../dashboard_tier2.html .
cp ../dashboard_tier1.html .

# Copy environment template
echo "⚙️ Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp ../.env_template .env
    echo "📝 Please edit .env file with your actual API keys and configuration"
    echo "   Required: OPENAI_API_KEY, MEM0_API_KEY, ANTHROPIC_API_KEY"
fi

# Create static directory and copy assets
echo "🎨 Setting up static assets..."
mkdir -p static
if [ -f "../objx-dark-background.svg" ]; then
    cp ../objx-dark-background.svg static/
fi
if [ -f "../objx-light-background.svg" ]; then
    cp ../objx-light-background.svg static/
fi

# Create templates directory
mkdir -p templates

# Create basic templates if they don't exist
if [ ! -f "templates/index.html" ]; then
    cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBJX Intelligence Platform</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            color: white;
            padding: 2rem;
        }
        .logo {
            font-size: 3rem;
            font-weight: 300;
            margin-bottom: 1rem;
        }
        .tagline {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">OBJX Intelligence</div>
        <div class="tagline">clarify • compound • create</div>
        <a href="/login" class="btn">Access Platform</a>
    </div>
</body>
</html>
EOF
fi

if [ ! -f "templates/login.html" ]; then
    cat > templates/login.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - OBJX Intelligence</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            font-size: 2rem;
            font-weight: 300;
            margin-bottom: 2rem;
            color: #333;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #555;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .demo-credentials {
            margin-top: 1rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">OBJX Intelligence</div>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Login</button>
        </form>
        <div class="demo-credentials">
            <strong>Demo Credentials:</strong><br>
            Admin: admin / admin123<br>
            Staff: staff / staff123
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else if (data.error) {
                    alert(data.error);
                }
            } catch (error) {
                alert('Login failed. Please try again.');
            }
        });
    </script>
</body>
</html>
EOF
fi

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "
import sys
sys.path.append('.')
from app import init_db
init_db()
print('Database initialized successfully')
"

# Create systemd service file (optional)
echo "🔧 Creating systemd service file..."
cat > objx-intelligence.service << EOF
[Unit]
Description=OBJX Intelligence Platform
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create startup script
echo "🚀 Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python app.py
EOF
chmod +x start.sh

# Create production startup script with gunicorn
cat > start_production.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
EOF
chmod +x start_production.sh

echo ""
echo "✅ OBJX Intelligence Platform deployment completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your actual API keys"
echo "2. Run: ./start.sh (for development)"
echo "3. Run: ./start_production.sh (for production)"
echo ""
echo "🌐 Default URLs:"
echo "   - Landing Page: http://localhost:5000"
echo "   - Login: http://localhost:5000/login"
echo "   - Admin Dashboard: http://localhost:5000/dashboard/admin"
echo "   - Staff Dashboard: http://localhost:5000/dashboard/staff"
echo ""
echo "🔑 Demo Credentials:"
echo "   - Admin: admin / admin123"
echo "   - Staff: staff / staff123"
echo ""
echo "📚 Documentation: See deployment documentation for advanced configuration"
echo ""
echo "🎯 OBJX Intelligence Platform is ready for deployment!"

