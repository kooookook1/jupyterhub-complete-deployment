# JupyterHub Debug Spawn Configuration

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12001

# Use DummyAuthenticator for development
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use SimpleLocalProcessSpawner with debug settings
from jupyterhub.spawner import SimpleLocalProcessSpawner
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

# Database configuration
c.JupyterHub.db_url = 'sqlite:///jupyterhub_debug_spawn.sqlite'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings - increased for debugging
c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 60

# Debug log level
c.Application.log_level = 'DEBUG'

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8083

# Proxy configuration
c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:8003'
c.ConfigurableHTTPProxy.pid_file = '/workspace/jupyterhub/proxy_debug_spawn.pid'

# Spawner debug settings
c.SimpleLocalProcessSpawner.debug = True

# Allow root for single-user servers
c.Spawner.args = ['--allow-root']

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

print("JupyterHub debug spawn configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print(f"Hub will run on port: {c.JupyterHub.hub_port}")
print("Log level: DEBUG (maximum verbosity)")
print("This will show detailed spawning information")