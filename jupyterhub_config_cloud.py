"""
JupyterHub configuration for cloud deployment (Railway, Render, Heroku)
"""
import os

# Network configuration for cloud deployment
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = int(os.environ.get('PORT', 8000))

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = int(os.environ.get('HUB_PORT', 8081))

# Proxy configuration
c.JupyterHub.proxy_api_port = int(os.environ.get('PROXY_API_PORT', 8001))

# Authentication
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = os.environ.get('ADMIN_PASSWORD', '')

# Spawner configuration for cloud
c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'
c.Spawner.args = ['--allow-root']
c.Spawner.default_url = '/lab'

# Timeouts
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 30

# Database
c.JupyterHub.db_url = os.environ.get('DATABASE_URL', 'sqlite:///jupyterhub.sqlite')

# Security
c.JupyterHub.cookie_secret_file = 'jupyterhub_cookie_secret'

# Logging
c.JupyterHub.log_level = 'INFO'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Concurrent spawn limit
c.JupyterHub.concurrent_spawn_limit = 10

print("🚀 JupyterHub Cloud Configuration Loaded!")
print(f"📡 Port: {c.JupyterHub.port}")
print(f"🔧 Hub Port: {c.JupyterHub.hub_port}")
print(f"🌐 Proxy API Port: {c.JupyterHub.proxy_api_port}")