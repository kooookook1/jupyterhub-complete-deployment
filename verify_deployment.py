#!/usr/bin/env python3
"""
JupyterHub Deployment Verification Script
تحقق من حالة تشغيل JupyterHub
"""

import requests
import subprocess
import sys
import time
from urllib.parse import urlparse

def check_process(process_name):
    """التحقق من وجود عملية معينة"""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], 
                              capture_output=True, text=True)
        return len(result.stdout.strip()) > 0
    except:
        return False

def check_port(port):
    """التحقق من أن المنفذ يستجيب"""
    try:
        response = requests.get(f'http://localhost:{port}', 
                              timeout=5, allow_redirects=False)
        return True
    except:
        return False

def check_jupyterhub_api():
    """التحقق من API الخاص بـ JupyterHub"""
    try:
        response = requests.get('http://localhost:8081/hub/api', 
                              timeout=5)
        return response.status_code in [200, 401, 403]
    except:
        return False

def main():
    print("🔍 التحقق من حالة تشغيل JupyterHub...")
    print("=" * 50)
    
    checks = []
    
    # التحقق من العمليات
    print("📋 التحقق من العمليات:")
    jupyterhub_running = check_process('jupyterhub')
    webserver_running = check_process('python.*http.server')
    proxy_running = check_process('configurable-http-proxy')
    
    checks.append(("JupyterHub Process", jupyterhub_running))
    checks.append(("Web Server Process", webserver_running))
    checks.append(("HTTP Proxy Process", proxy_running))
    
    print(f"  JupyterHub: {'✅' if jupyterhub_running else '❌'}")
    print(f"  Web Server: {'✅' if webserver_running else '❌'}")
    print(f"  HTTP Proxy: {'✅' if proxy_running else '❌'}")
    
    # التحقق من المنافذ
    print("\n🌐 التحقق من المنافذ:")
    port_12000 = check_port(12000)
    port_12001 = check_port(12001)
    port_8081 = check_port(8081)
    
    checks.append(("Port 12000 (JupyterHub)", port_12000))
    checks.append(("Port 12001 (Web Server)", port_12001))
    checks.append(("Port 8081 (Hub API)", port_8081))
    
    print(f"  Port 12000 (JupyterHub): {'✅' if port_12000 else '❌'}")
    print(f"  Port 12001 (Web Server): {'✅' if port_12001 else '❌'}")
    print(f"  Port 8081 (Hub API): {'✅' if port_8081 else '❌'}")
    
    # التحقق من API
    print("\n🔌 التحقق من APIs:")
    api_working = check_jupyterhub_api()
    checks.append(("JupyterHub API", api_working))
    print(f"  JupyterHub API: {'✅' if api_working else '❌'}")
    
    # التحقق من الملفات
    print("\n📁 التحقق من الملفات:")
    import os
    files_to_check = [
        'jupyterhub_config_custom.py',
        'jupyterhub.sqlite',
        'jupyterhub.log',
        'test_access.html',
        'DEPLOYMENT_README.md'
    ]
    
    for file in files_to_check:
        exists = os.path.exists(file)
        checks.append((f"File: {file}", exists))
        print(f"  {file}: {'✅' if exists else '❌'}")
    
    # النتيجة النهائية
    print("\n" + "=" * 50)
    total_checks = len(checks)
    passed_checks = sum(1 for _, status in checks if status)
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"📊 النتيجة النهائية:")
    print(f"  الاختبارات المجتازة: {passed_checks}/{total_checks}")
    print(f"  نسبة النجاح: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🎉 ممتاز! JupyterHub يعمل بنجاح!")
        print("🌐 الروابط:")
        print("  JupyterHub: https://work-1-uqtcepzjstktaouv.prod-runtime.all-hands.dev")
        print("  معلومات: https://work-2-uqtcepzjstktaouv.prod-runtime.all-hands.dev")
        return 0
    elif success_rate >= 70:
        print("\n⚠️  JupyterHub يعمل مع بعض المشاكل")
        return 1
    else:
        print("\n❌ هناك مشاكل في تشغيل JupyterHub")
        return 2

if __name__ == "__main__":
    sys.exit(main())