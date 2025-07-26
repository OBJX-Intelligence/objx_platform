# OBJX Intelligence Platform - Installation Guide

## System Requirements
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Step-by-Step Installation

### 1. Extract Package
```bash
# If you received a zip file, extract it:
unzip objx_complete_package.zip
cd objx_complete_package
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv objx_env
source objx_env/bin/activate  # On Windows: objx_env\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example backend/.env

# Edit the .env file with your API keys
nano backend/.env  # or use your preferred editor
```

Required API Keys:
- **OpenAI API Key**: Get from https://platform.openai.com/api-keys
- **MEM0 API Key**: Get from https://app.mem0.ai (optional, for memory features)

### 5. Verify File Structure
Your directory should look like this:
```
objx_complete_package/
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard_tier1.html
│   ├── dashboard_tier2.html
│   └── dashboard_tier3.html
├── backend/
│   ├── app.py
│   ├── agents.py
│   └── .env
├── assets/
│   ├── objx-light-background.svg
│   └── objx-dark-background.svg
├── docs/
│   └── [foundation documents]
└── requirements.txt
```

### 6. Start the Server
```bash
cd backend
python app.py
```

You should see output like:
```
🚀 OBJX PLATFORM - SELF-CONTAINED VERSION
============================================================
🧠 Trinity Architecture: Foundation + mem0 + Systematic Thinking
📊 Testing Validated: Foundation superiority proven
🔧 Optimized: No exchange prompt, natural intelligence flow
============================================================
📚 Foundation Documents: X/6 loaded
🔑 OpenAI API: ✅ Configured
🧠 MEM0 API: ✅ Configured
============================================================
🌐 Starting server on http://localhost:5000
```

### 7. Access the Platform
Open your web browser and navigate to:
```
http://localhost:5000
```

## Testing the Installation

### 1. Landing Page Test
- Verify the landing page loads with OBJX branding
- Test theme toggle (🌙 ↔ ☀️)
- Check that all sections are visible
- Test "Access Platform" button

### 2. Dashboard Test
- Navigate to login page
- Access dashboard tiers (tier1, tier2, tier3)
- Verify all animations and interactions work

### 3. Scaling Test
- Check if content displays at proper size
- Test on different screen resolutions
- Verify mobile responsiveness

## Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill any process using port 5000
sudo lsof -ti:5000 | xargs kill -9
```

**2. Missing Dependencies**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

**3. API Key Issues**
- Verify your OpenAI API key is valid
- Check that the .env file is in the backend directory
- Ensure no extra spaces in API key values

**4. Scaling Issues**
The platform includes automatic device pixel ratio detection and compensation. If scaling issues persist, check browser zoom settings.

**5. File Permissions**
```bash
# Ensure proper permissions
chmod +x backend/app.py
```

## Development Mode

For development, you can run with debug mode:
```bash
export FLASK_DEBUG=1
cd backend
python app.py
```

## Production Deployment

For production deployment:
1. Set `FLASK_ENV=production` in .env
2. Use a production WSGI server like Gunicorn
3. Configure proper security headers
4. Set up SSL/HTTPS

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure API keys are properly configured
4. Test with a fresh browser session

The platform has been tested and verified working with all features functional.

