#!/bin/bash

echo "🚀 JupyterHub Complete Deployment - Installation Script"
echo "======================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo "✅ Node.js found: $(node --version)"
echo "✅ npm found: $(npm --version)"

echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "📦 Installing Node.js dependencies..."
npm install

echo ""
echo "📦 Installing configurable-http-proxy globally..."
npm install -g configurable-http-proxy

echo ""
echo "🔧 Setting up permissions..."
chmod +x start_jupyterhub.sh
chmod +x setup_complete_deployment.sh

echo ""
echo "🧪 Running functionality tests..."
python3 test_complete_functionality.py

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 To start JupyterHub, run:"
echo "   ./start_jupyterhub.sh"
echo ""
echo "🌐 Then open your browser and go to:"
echo "   http://localhost:12001"
echo ""
echo "👤 Login with:"
echo "   Username: admin (or any name)"
echo "   Password: (leave empty)"