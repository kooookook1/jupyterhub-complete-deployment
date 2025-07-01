#!/bin/bash

# JupyterHub Startup Script - Production Ready
# This script starts JupyterHub with the verified working configuration

echo "🚀 Starting JupyterHub Production Server..."
echo "=" * 60

# Kill any existing JupyterHub processes
echo "🧹 Cleaning up existing processes..."
pkill -f jupyterhub 2>/dev/null || true
sleep 2

# Change to JupyterHub directory
cd /workspace/jupyterhub

# Start JupyterHub with production configuration
echo "🌟 Starting JupyterHub..."
jupyterhub --config=jupyterhub_config_production.py > jupyterhub_production.log 2>&1 &

# Wait for startup
sleep 5

# Check if JupyterHub is running
if pgrep -f jupyterhub > /dev/null; then
    echo "✅ JupyterHub started successfully!"
    echo "🌐 Access URL: https://work-2-uqtcepzjstktaouv.prod-runtime.all-hands.dev"
    echo "👤 Login: username=admin, password=(empty)"
    echo "📋 Log file: jupyterhub_production.log"
    echo "🔧 Configuration: jupyterhub_config_production.py"
    echo ""
    echo "🎉 JupyterHub is ready for use!"
else
    echo "❌ Failed to start JupyterHub"
    echo "📋 Check log file: jupyterhub_production.log"
    exit 1
fi