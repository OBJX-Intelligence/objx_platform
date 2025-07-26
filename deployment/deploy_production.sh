#!/bin/bash

# OBJX Intelligence Platform - Production Deployment Script
# Author: Manus AI
# Date: July 25, 2025
# Version: 1.0 - Production Ready

set -e

echo "🚀 OBJX Intelligence Platform - Production Deployment"
echo "====================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    echo "Please install Docker and Docker Compose first"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed"
    echo "Please install Docker Compose first"
    exit 1
fi

# Create production directory
DEPLOY_DIR="objx_production"
echo "📁 Creating production directory: $DEPLOY_DIR"
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Copy deployment files
echo "📋 Copying deployment files..."
cp ../objx_deployment_app.py .
cp ../requirements_deployment.txt .
cp ../Dockerfile .
cp ../docker-compose.yml .
cp ../nginx.conf .
cp ../dashboard_*.html .

# Copy static assets
mkdir -p static templates
if [ -f "../objx-dark-background.svg" ]; then
    cp ../objx-dark-background.svg static/
fi
if [ -f "../objx-light-background.svg" ]; then
    cp ../objx-light-background.svg static/
fi

# Create environment file
echo "⚙️ Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# OBJX Intelligence Platform - Production Environment
SECRET_KEY=change-this-secret-key-in-production
FLASK_ENV=production
PORT=5000

# API Keys (REQUIRED - Add your actual keys)
OPENAI_API_KEY=your-openai-api-key-here
MEM0_API_KEY=your-mem0-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Google Workspace (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# QuickBooks (Optional - Admin only)
QUICKBOOKS_CLIENT_ID=your-quickbooks-client-id
QUICKBOOKS_CLIENT_SECRET=your-quickbooks-client-secret

# Database
DATABASE_URL=sqlite:///data/objx_platform.db

# Security
SESSION_TIMEOUT=3600
PASSWORD_MIN_LENGTH=8
EOF
    echo "📝 Please edit .env file with your actual API keys"
fi

# Create data and logs directories
mkdir -p data logs ssl

# Create SSL certificate (self-signed for development)
if [ ! -f "ssl/cert.pem" ]; then
    echo "🔒 Creating self-signed SSL certificate..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=OBJX/CN=localhost"
fi

# Create production startup script
cat > start_production.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting OBJX Intelligence Platform in production mode..."

# Pull latest images
docker-compose pull

# Build and start services
docker-compose up --build -d

echo "✅ OBJX Intelligence Platform started successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   - HTTPS: https://localhost"
echo "   - HTTP: http://localhost (redirects to HTTPS)"
echo ""
echo "📊 Monitoring:"
echo "   - Health Check: https://localhost/health"
echo "   - Logs: docker-compose logs -f"
echo ""
echo "🔧 Management:"
echo "   - Stop: docker-compose down"
echo "   - Restart: docker-compose restart"
echo "   - Update: docker-compose pull && docker-compose up -d"
EOF
chmod +x start_production.sh

# Create management scripts
cat > stop.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping OBJX Intelligence Platform..."
docker-compose down
echo "✅ Platform stopped successfully"
EOF
chmod +x stop.sh

cat > logs.sh << 'EOF'
#!/bin/bash
echo "📊 OBJX Intelligence Platform Logs:"
echo "=================================="
docker-compose logs -f
EOF
chmod +x logs.sh

cat > update.sh << 'EOF'
#!/bin/bash
echo "🔄 Updating OBJX Intelligence Platform..."
docker-compose pull
docker-compose up --build -d
echo "✅ Platform updated successfully"
EOF
chmod +x update.sh

# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "💾 Creating backup..."
cp -r data $BACKUP_DIR/
cp .env $BACKUP_DIR/
cp -r ssl $BACKUP_DIR/

echo "✅ Backup created: $BACKUP_DIR"
EOF
chmod +x backup.sh

# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "📊 OBJX Intelligence Platform Status:"
echo "===================================="
echo ""

# Check if services are running
echo "🔍 Service Status:"
docker-compose ps

echo ""
echo "💾 Disk Usage:"
df -h | grep -E "(Filesystem|/dev/)"

echo ""
echo "🔗 Health Check:"
curl -s https://localhost/health | jq . 2>/dev/null || echo "Health check failed"

echo ""
echo "📈 Resource Usage:"
docker stats --no-stream
EOF
chmod +x monitor.sh

echo ""
echo "✅ OBJX Intelligence Platform production deployment completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your actual API keys"
echo "2. Run: ./start_production.sh"
echo ""
echo "🔧 Management Commands:"
echo "   - Start: ./start_production.sh"
echo "   - Stop: ./stop.sh"
echo "   - Logs: ./logs.sh"
echo "   - Update: ./update.sh"
echo "   - Backup: ./backup.sh"
echo "   - Monitor: ./monitor.sh"
echo ""
echo "🌐 Access URLs (after starting):"
echo "   - HTTPS: https://localhost"
echo "   - Health: https://localhost/health"
echo ""
echo "🔑 Demo Credentials:"
echo "   - Admin: admin / admin123"
echo "   - Staff: staff / staff123"
echo ""
echo "🎯 OBJX Intelligence Platform is ready for production deployment!"

