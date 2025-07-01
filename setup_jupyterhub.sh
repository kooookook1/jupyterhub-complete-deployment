#!/bin/bash
# JupyterHub Setup Script
# سكريبت إعداد JupyterHub

set -e

echo "🚀 بدء إعداد JupyterHub..."

# التحقق من المتطلبات
echo "📋 التحقق من المتطلبات..."

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    exit 1
fi

# التحقق من Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js غير مثبت"
    exit 1
fi

# التحقق من npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm غير مثبت"
    exit 1
fi

echo "✅ جميع المتطلبات متوفرة"

# تثبيت configurable-http-proxy
echo "📦 تثبيت configurable-http-proxy..."
npm install -g configurable-http-proxy

# تثبيت متطلبات Python
echo "📦 تثبيت متطلبات Python..."
pip install -r requirements.txt
pip install jupyterlab notebook

# تثبيت JupyterHub من المصدر
echo "📦 تثبيت JupyterHub..."
pip install -e .

# تثبيت متطلبات Node.js
echo "📦 تثبيت متطلبات Node.js..."
npm install

# بناء CSS
echo "🎨 بناء CSS..."
npm run css

# بناء JSX
echo "⚛️ بناء JSX..."
npm run jsx:install-run
npm run jsx:run build

# إنشاء ملف التكوين إذا لم يكن موجوداً
if [ ! -f "jupyterhub_config_custom.py" ]; then
    echo "⚙️ إنشاء ملف التكوين..."
    cat > jupyterhub_config_custom.py << 'EOF'
# JupyterHub configuration for development environment

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator

# Allow any username
c.DummyAuthenticator.password = ""

# Spawner configuration
from jupyterhub.spawner import LocalProcessSpawner
c.JupyterHub.spawner_class = LocalProcessSpawner

# Allow users to create their own accounts
c.LocalAuthenticator.create_system_users = False

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Admin users (optional)
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 30

# Log level
c.Application.log_level = 'INFO'

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'

# Proxy configuration
c.ConfigurableHTTPProxy.should_start = True

# Allow iframe embedding
c.JupyterHub.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors 'self' *"
    }
}

print("JupyterHub configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Authentication: DummyAuthenticator (any username, no password)")
EOF
fi

echo "✅ تم إعداد JupyterHub بنجاح!"
echo ""
echo "🚀 لتشغيل JupyterHub:"
echo "   jupyterhub --config=jupyterhub_config_custom.py"
echo ""
echo "🌐 الوصول إلى JupyterHub:"
echo "   http://localhost:12000"
echo ""
echo "🔐 تسجيل الدخول:"
echo "   اسم المستخدم: أي اسم (مثل: admin)"
echo "   كلمة المرور: اتركها فارغة"