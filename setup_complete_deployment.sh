#!/bin/bash

# JupyterHub Complete Deployment Setup Script
# This script sets up a complete working JupyterHub deployment

echo "🚀 JupyterHub Complete Deployment Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "Running as root. This is okay for containers but not recommended for production."
fi

# Update system packages (if needed)
print_info "Checking system requirements..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
    print_status "Python $python_version is compatible"
else
    print_error "Python 3.8+ required. Current version: $python_version"
    exit 1
fi

# Install system dependencies
print_info "Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    apt-get update -qq
    apt-get install -y python3-pip nodejs npm curl wget
elif command -v yum &> /dev/null; then
    yum install -y python3-pip nodejs npm curl wget
elif command -v brew &> /dev/null; then
    brew install python3 node npm
fi

# Install configurable-http-proxy
print_info "Installing configurable-http-proxy..."
if ! command -v configurable-http-proxy &> /dev/null; then
    npm install -g configurable-http-proxy
    print_status "configurable-http-proxy installed"
else
    print_status "configurable-http-proxy already installed"
fi

# Install Python dependencies
print_info "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt
print_status "Python dependencies installed"

# Install Node.js dependencies (if package.json exists)
if [ -f "package.json" ]; then
    print_info "Installing Node.js dependencies..."
    npm install
    print_status "Node.js dependencies installed"
fi

# Create necessary directories
print_info "Creating directories..."
mkdir -p runtime data logs
print_status "Directories created"

# Set permissions
print_info "Setting permissions..."
chmod +x start_jupyterhub.sh
chmod +x setup_complete_deployment.sh
print_status "Permissions set"

# Generate cookie secret if not exists
if [ ! -f "jupyterhub_cookie_secret" ]; then
    print_info "Generating cookie secret..."
    openssl rand -hex 32 > jupyterhub_cookie_secret
    chmod 600 jupyterhub_cookie_secret
    print_status "Cookie secret generated"
fi

# Test installation
print_info "Testing installation..."
if python3 -c "import jupyterhub; print('JupyterHub version:', jupyterhub.__version__)" 2>/dev/null; then
    print_status "JupyterHub installation verified"
else
    print_error "JupyterHub installation failed"
    exit 1
fi

# Run functionality test
print_info "Running functionality test..."
if python3 test_complete_functionality.py > /dev/null 2>&1; then
    print_status "All functionality tests passed"
else
    print_warning "Some tests failed. Check test_complete_functionality.py output"
fi

# Final setup
print_info "Final setup..."

# Create systemd service file (optional)
cat > jupyterhub.service << EOF
[Unit]
Description=JupyterHub
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(which jupyterhub) --config=jupyterhub_config_production.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_status "Systemd service file created (jupyterhub.service)"

# Create Docker files
cat > Dockerfile << EOF
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    nodejs npm curl wget \\
    && rm -rf /var/lib/apt/lists/*

# Install configurable-http-proxy
RUN npm install -g configurable-http-proxy

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p runtime data logs

# Set permissions
RUN chmod +x start_jupyterhub.sh

# Expose port
EXPOSE 12001

# Start JupyterHub
CMD ["jupyterhub", "--config=jupyterhub_config_production.py"]
EOF

cat > docker-compose.yml << EOF
version: '3.8'

services:
  jupyterhub:
    build: .
    ports:
      - "12001:12001"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - JUPYTERHUB_CRYPT_KEY=\${JUPYTERHUB_CRYPT_KEY:-$(openssl rand -hex 32)}
    restart: unless-stopped
EOF

print_status "Docker files created"

# Summary
echo ""
echo "🎉 Setup Complete!"
echo "=================="
print_status "JupyterHub is ready for deployment"
print_info "Configuration file: jupyterhub_config_production.py"
print_info "Startup script: ./start_jupyterhub.sh"
print_info "Test script: python3 test_complete_functionality.py"
print_info "Service URL: http://localhost:12001"
print_info "Default user: admin (no password)"

echo ""
echo "🚀 Quick Start:"
echo "  ./start_jupyterhub.sh"
echo ""
echo "🐳 Docker Start:"
echo "  docker-compose up -d"
echo ""
echo "🔧 Systemd Service:"
echo "  sudo cp jupyterhub.service /etc/systemd/system/"
echo "  sudo systemctl enable jupyterhub"
echo "  sudo systemctl start jupyterhub"
echo ""

print_status "Setup completed successfully!"