# JupyterHub Ultimate Configuration - Final Working Solution

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use LocalProcessSpawner with proper configuration
from jupyterhub.spawner import LocalProcessSpawner

# Override LocalProcessSpawner to work without system users
class UltimateSpawner(LocalProcessSpawner):
    """Ultimate spawner that works in any environment"""
    
    def user_env(self, env):
        """Override to set proper environment"""
        # Don't call super() to avoid system user checks
        env = env.copy()
        env.update({
            'USER': 'root',
            'HOME': '/workspace/jupyterhub',
            'SHELL': '/bin/bash',
            'PATH': '/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin:/usr/local/bin:/usr/bin:/bin',
            'JUPYTER_RUNTIME_DIR': '/workspace/jupyterhub/runtime',
            'JUPYTER_DATA_DIR': '/workspace/jupyterhub/data',
            'JUPYTERHUB_USER': self.user.name,
            'JUPYTERHUB_BASE_URL': self.user.server.base_url,
            'JUPYTERHUB_SERVICE_PREFIX': self.user.server.base_url,
        })
        return env
    
    def get_args(self):
        """Override to set proper arguments"""
        args = []
        args.extend([
            '--ip=0.0.0.0',
            '--port={port}',
            '--notebook-dir=/workspace/jupyterhub',
            '--allow-root',
            '--NotebookApp.allow_origin="*"',
            '--NotebookApp.disable_check_xsrf=True',
            '--debug'
        ])
        return args

c.JupyterHub.spawner_class = UltimateSpawner

# Set the command to run
c.Spawner.cmd = ['/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin/jupyterhub-singleuser']

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings
c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 60

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

# Create runtime directories
import os
os.makedirs('/workspace/jupyterhub/runtime', exist_ok=True)
os.makedirs('/workspace/jupyterhub/data', exist_ok=True)

print("JupyterHub ultimate configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Authentication: DummyAuthenticator (any username, no password)")
print("Spawner: UltimateSpawner (LocalProcessSpawner without system user requirements)")
print("Command: jupyterhub-singleuser with proper arguments")
print("Timeout: 120 seconds for startup")