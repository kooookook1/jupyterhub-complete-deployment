# JupyterHub Debug Configuration - High Verbosity

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use SimpleLocalProcessSpawner with debug
from jupyterhub.spawner import SimpleLocalProcessSpawner
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub_debug.sqlite'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 30

# DEBUG LOG LEVEL
c.Application.log_level = 'DEBUG'

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'

# Proxy configuration
c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.pid_file = '/workspace/jupyterhub/proxy_debug.pid'

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

print("JupyterHub debug configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Log level: DEBUG (maximum verbosity)")
print("This will show detailed spawning information")