#!/usr/bin/env python3
"""
JupyterHub Vercel Deployment App
This is a simplified version for Vercel deployment
"""

from flask import Flask, render_template_string, request, redirect, session
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('JUPYTERHUB_CRYPT_KEY', secrets.token_hex(32))

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>JupyterHub</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
        .logo h1 {
            color: #f37626;
            margin: 0;
            font-size: 2rem;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #333;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
            box-sizing: border-box;
        }
        .btn {
            background: #f37626;
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
        }
        .btn:hover {
            background: #e55a0c;
        }
        .status {
            text-align: center;
            margin-top: 1rem;
            padding: 1rem;
            background: #e8f5e8;
            border-radius: 5px;
            color: #2d5a2d;
        }
        .warning {
            background: #fff3cd;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>🚀 JupyterHub</h1>
            <p>Complete Deployment</p>
        </div>
        
        <div class="warning">
            <strong>⚠️ ملاحظة مهمة:</strong><br>
            هذا عرض توضيحي لـ JupyterHub على Vercel. للحصول على الوظائف الكاملة، يرجى تشغيل المشروع محلياً.
        </div>
        
        <form method="post" action="/login">
            <div class="form-group">
                <label for="username">اسم المستخدم:</label>
                <input type="text" id="username" name="username" placeholder="admin" required>
            </div>
            <div class="form-group">
                <label for="password">كلمة المرور:</label>
                <input type="password" id="password" name="password" placeholder="(اتركها فارغة)">
            </div>
            <button type="submit" class="btn">تسجيل الدخول</button>
        </form>
        
        <div class="status">
            <strong>✅ الحالة:</strong> JupyterHub متاح للتحميل والتشغيل المحلي<br>
            <strong>🌐 GitHub:</strong> <a href="https://github.com/kooookook1/jupyterhub-complete-deployment" target="_blank">تحميل المشروع الكامل</a>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>JupyterHub - Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            margin: 0;
            padding: 2rem;
        }
        .header {
            background: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo h1 {
            color: #f37626;
            margin: 0;
        }
        .user-info {
            color: #666;
        }
        .card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .btn {
            background: #f37626;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            display: inline-block;
            margin: 0.5rem 0.5rem 0.5rem 0;
        }
        .btn:hover {
            background: #e55a0c;
        }
        .btn-secondary {
            background: #6c757d;
        }
        .btn-secondary:hover {
            background: #545b62;
        }
        .status-good {
            color: #28a745;
            font-weight: bold;
        }
        .instructions {
            background: #e3f2fd;
            padding: 1.5rem;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <h1>🚀 JupyterHub Dashboard</h1>
        </div>
        <div class="user-info">
            مرحباً، {{ username }}! | <a href="/logout">تسجيل الخروج</a>
        </div>
    </div>
    
    <div class="card">
        <h2>📊 حالة النظام</h2>
        <p><strong>الحالة:</strong> <span class="status-good">✅ متاح للتحميل والتشغيل</span></p>
        <p><strong>المنصة:</strong> Vercel (عرض توضيحي)</p>
        <p><strong>الإصدار:</strong> JupyterHub Complete Deployment v1.0</p>
    </div>
    
    <div class="card">
        <h2>🚀 بدء خادم Jupyter</h2>
        <p>لبدء خادم Jupyter الخاص بك، يرجى تحميل المشروع وتشغيله محلياً:</p>
        
        <div class="instructions">
            <h3>📥 خطوات التشغيل المحلي:</h3>
            <ol>
                <li>حمل المشروع من GitHub</li>
                <li>شغل: <code>chmod +x install.sh && ./install.sh</code></li>
                <li>شغل: <code>./start_jupyterhub.sh</code></li>
                <li>افتح: <code>http://localhost:12001</code></li>
            </ol>
        </div>
        
        <a href="https://github.com/kooookook1/jupyterhub-complete-deployment" target="_blank" class="btn">
            📥 تحميل المشروع الكامل
        </a>
        <a href="/demo-notebook" class="btn btn-secondary">
            📓 عرض توضيحي للـ Notebook
        </a>
    </div>
    
    <div class="card">
        <h2>📚 الموارد والتوثيق</h2>
        <p>جميع الملفات والتوثيق متاح في مستودع GitHub:</p>
        <ul>
            <li><strong>README_START_HERE.md</strong> - دليل البداية السريعة</li>
            <li><strong>QUICK_START_GUIDE.md</strong> - دليل التثبيت المفصل</li>
            <li><strong>test_complete_functionality.py</strong> - اختبارات شاملة</li>
            <li><strong>jupyterhub_config_production.py</strong> - تكوين الإنتاج</li>
        </ul>
    </div>
</body>
</html>
"""

NOTEBOOK_DEMO_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>JupyterHub - Notebook Demo</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            margin: 0;
            padding: 2rem;
        }
        .header {
            background: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .notebook {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .cell {
            border-bottom: 1px solid #eee;
            padding: 1rem;
        }
        .cell-input {
            background: #f8f9fa;
            padding: 1rem;
            border-left: 3px solid #007bff;
            font-family: 'Monaco', 'Consolas', monospace;
            margin-bottom: 0.5rem;
        }
        .cell-output {
            background: #fff;
            padding: 1rem;
            border-left: 3px solid #28a745;
            font-family: 'Monaco', 'Consolas', monospace;
        }
        .btn {
            background: #f37626;
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            display: inline-block;
            margin: 0.5rem 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📓 Jupyter Notebook - عرض توضيحي</h1>
        <a href="/dashboard" class="btn">← العودة إلى Dashboard</a>
    </div>
    
    <div class="notebook">
        <div class="cell">
            <div class="cell-input">
# مرحباً بك في JupyterHub!
print("🚀 JupyterHub Complete Deployment")
print("✅ النظام يعمل بنجاح!")

# معلومات النظام
import sys
print(f"🐍 Python Version: {sys.version}")
            </div>
            <div class="cell-output">
🚀 JupyterHub Complete Deployment
✅ النظام يعمل بنجاح!
🐍 Python Version: 3.9.0 (default, Oct  9 2020, 15:07:54)
            </div>
        </div>
        
        <div class="cell">
            <div class="cell-input">
# اختبار العمليات الحسابية
import numpy as np
import matplotlib.pyplot as plt

# إنشاء بيانات تجريبية
x = np.linspace(0, 10, 100)
y = np.sin(x)

print("📊 تم إنشاء البيانات بنجاح!")
print(f"📈 عدد النقاط: {len(x)}")
            </div>
            <div class="cell-output">
📊 تم إنشاء البيانات بنجاح!
📈 عدد النقاط: 100
            </div>
        </div>
        
        <div class="cell">
            <div class="cell-input">
# للحصول على الوظائف الكاملة، حمل المشروع وشغله محلياً:
print("📥 تحميل المشروع:")
print("git clone https://github.com/kooookook1/jupyterhub-complete-deployment.git")
print("\n🔧 التثبيت:")
print("chmod +x install.sh && ./install.sh")
print("\n🚀 التشغيل:")
print("./start_jupyterhub.sh")
print("\n🌐 الوصول:")
print("http://localhost:12001")
            </div>
            <div class="cell-output">
📥 تحميل المشروع:
git clone https://github.com/kooookook1/jupyterhub-complete-deployment.git

🔧 التثبيت:
chmod +x install.sh && ./install.sh

🚀 التشغيل:
./start_jupyterhub.sh

🌐 الوصول:
http://localhost:12001
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', 'admin')
    # Simple authentication - accept any username
    session['username'] = username
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template_string(DASHBOARD_TEMPLATE, username=session['username'])

@app.route('/demo-notebook')
def demo_notebook():
    if 'username' not in session:
        return redirect('/')
    return render_template_string(NOTEBOOK_DEMO_TEMPLATE)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/hub')
def hub():
    return redirect('/dashboard')

@app.route('/hub/home')
def hub_home():
    return redirect('/dashboard')

# API endpoints for compatibility
@app.route('/hub/api/users')
def api_users():
    return {
        "users": [
            {
                "name": session.get('username', 'admin'),
                "admin": True,
                "server": "/user/" + session.get('username', 'admin') + "/",
                "pending": None,
                "created": "2024-01-01T00:00:00.000Z",
                "last_activity": "2024-01-01T00:00:00.000Z"
            }
        ]
    }

@app.route('/hub/api/info')
def api_info():
    return {
        "version": "5.0.0",
        "python": "3.9.0",
        "sys_executable": "/usr/bin/python3",
        "authenticator": {
            "class": "DummyAuthenticator",
            "version": "1.0.0"
        },
        "spawner": {
            "class": "SimpleLocalProcessSpawner",
            "version": "1.0.0"
        }
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))