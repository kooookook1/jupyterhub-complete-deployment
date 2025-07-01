# JupyterHub Final Configuration - Working Solution

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use LocalProcessSpawner with custom configuration
from jupyterhub.spawner import LocalProcessSpawner

class CustomLocalProcessSpawner(LocalProcessSpawner):
    """Custom spawner that works without system users"""
    
    def user_env(self, env):
        """Override to set custom environment"""
        env = super().user_env(env)
        env.update({
            'USER': 'root',
            'HOME': '/workspace/jupyterhub',
            'SHELL': '/bin/bash',
            'PATH': '/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin:/usr/local/bin:/usr/bin:/bin',
            'JUPYTER_RUNTIME_DIR': '/workspace/jupyterhub/runtime',
            'JUPYTER_DATA_DIR': '/workspace/jupyterhub/data'
        })
        return env
    
    def get_args(self):
        """Override to set custom arguments"""
        args = super().get_args()
        args.extend([
            '--allow-root',
            '--ip=0.0.0.0',
            '--port={port}',
            '--notebook-dir=/workspace/jupyterhub',
            '--debug'
        ])
        return args

c.JupyterHub.spawner_class = CustomLocalProcessSpawner

# Set the command to run jupyterhub-singleuser
c.Spawner.cmd = ['/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin/jupyterhub-singleuser']

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings - increase for debugging
c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 60

# Log level
c.Application.log_level = 'DEBUG'

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

# Create runtime directories
import os
os.makedirs('/workspace/jupyterhub/runtime', exist_ok=True)
os.makedirs('/workspace/jupyterhub/data', exist_ok=True)

print("JupyterHub final configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Authentication: DummyAuthenticator (any username, no password)")
print("Spawner: CustomLocalProcessSpawner")
print("Timeout: 120 seconds for startup")