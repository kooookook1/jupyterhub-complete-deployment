# JupyterHub Final Working Configuration - Different Ports

c = get_config()

# Network configuration - use different port to avoid conflicts
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12001  # Changed from 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use SimpleLocalProcessSpawner
from jupyterhub.spawner import SimpleLocalProcessSpawner
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub_final.sqlite'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 30

# Log level
c.Application.log_level = 'INFO'

# Hub configuration - use different port
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8082  # Changed from 8081

# Proxy configuration - use different API port
c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:8002'  # Changed from 8001
c.ConfigurableHTTPProxy.pid_file = '/workspace/jupyterhub/proxy_final.pid'

# Allow iframe embedding
c.JupyterHub.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors 'self' *"
    }
}

# Create runtime directories
import os
os.makedirs('/workspace/jupyterhub/runtime', exist_ok=True)
os.makedirs('/workspace/jupyterhub/data', exist_ok=True)

print("JupyterHub final working configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print(f"Hub will run on port: {c.JupyterHub.hub_port}")
print("Authentication: DummyAuthenticator (any username, no password)")
print("Spawner: SimpleLocalProcessSpawner")
print("Using different ports to avoid conflicts")