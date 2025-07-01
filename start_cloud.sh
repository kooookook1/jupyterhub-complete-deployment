#!/bin/bash

echo "🚀 Starting JupyterHub for Cloud Deployment..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Generate cookie secret if not exists
if [ ! -f "jupyterhub_cookie_secret" ]; then
    echo "🔐 Generating cookie secret..."
    openssl rand -hex 32 > jupyterhub_cookie_secret
fi

# Set default port if not set
export PORT=${PORT:-8000}
export HUB_PORT=${HUB_PORT:-8081}
export PROXY_API_PORT=${PROXY_API_PORT:-8001}

echo "🌐 Starting JupyterHub on port $PORT..."
echo "🔧 Hub port: $HUB_PORT"
echo "📡 Proxy API port: $PROXY_API_PORT"

# Start JupyterHub
jupyterhub --config=jupyterhub_config_cloud.py