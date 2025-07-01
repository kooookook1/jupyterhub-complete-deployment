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

# Spawner configuration - use LocalProcessSpawner but run as current user
from jupyterhub.spawner import LocalProcessSpawner
c.JupyterHub.spawner_class = LocalProcessSpawner

# Allow users to create their own accounts
c.LocalAuthenticator.create_system_users = False

# Configure spawner to work in development environment
import os
import pwd

# Get current user info
current_user = pwd.getpwuid(os.getuid())

# Override the get_env method to use current user
def get_env_override(self):
    env = super(LocalProcessSpawner, self).get_env()
    env.update({
        'USER': current_user.pw_name,
        'HOME': '/workspace/jupyterhub',
        'SHELL': '/bin/bash',
        'PATH': '/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin:/usr/local/bin:/usr/bin:/bin'
    })
    return env

# Monkey patch the spawner
LocalProcessSpawner.get_env = get_env_override

# Set the command to run
c.Spawner.cmd = ['/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin/jupyterhub-singleuser']
c.Spawner.args = ['--allow-root']

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

# CORS settings
c.JupyterHub.extra_handlers = []

print("JupyterHub configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Authentication: DummyAuthenticator (any username, no password)")