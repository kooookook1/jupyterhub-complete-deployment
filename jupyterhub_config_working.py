# JupyterHub Working Configuration - Tested Solution

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use SystemdSpawner alternative - create a simple working spawner
from jupyterhub.spawner import Spawner
import subprocess
import os
import signal
import time
from tornado import gen

class WorkingSpawner(Spawner):
    """A simple spawner that actually works"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.proc = None
        self.pid = None
    
    @gen.coroutine
    def start(self):
        """Start the single-user server"""
        # Create a unique port for this user
        import random
        port = random.randint(50000, 60000)
        
        # Set up environment
        env = os.environ.copy()
        env.update({
            'USER': 'root',
            'HOME': '/workspace/jupyterhub',
            'SHELL': '/bin/bash',
            'PATH': '/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin:/usr/local/bin:/usr/bin:/bin',
            'JUPYTER_RUNTIME_DIR': '/workspace/jupyterhub/runtime',
            'JUPYTER_DATA_DIR': '/workspace/jupyterhub/data'
        })
        
        # Command to run
        cmd = [
            '/openhands/poetry/openhands-ai-5O4_aCHf-py3.12/bin/python',
            '-m', 'jupyter', 'lab',
            '--allow-root',
            '--ip=0.0.0.0',
            f'--port={port}',
            '--notebook-dir=/workspace/jupyterhub',
            '--no-browser',
            '--NotebookApp.token=""',
            '--NotebookApp.password=""',
            '--NotebookApp.disable_check_xsrf=True',
            f'--NotebookApp.base_url=/user/{self.user.name}/',
            '--debug'
        ]
        
        # Start the process
        self.proc = subprocess.Popen(
            cmd,
            env=env,
            cwd='/workspace/jupyterhub',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.pid = self.proc.pid
        
        # Wait a bit for startup
        yield gen.sleep(3)
        
        # Return the URL info
        return {
            'ip': '0.0.0.0',
            'port': port,
            'pid': self.pid
        }
    
    @gen.coroutine
    def stop(self, now=False):
        """Stop the single-user server"""
        if self.proc:
            try:
                if now:
                    self.proc.kill()
                else:
                    self.proc.terminate()
                    # Wait for graceful shutdown
                    for i in range(10):
                        if self.proc.poll() is not None:
                            break
                        yield gen.sleep(0.5)
                    else:
                        # Force kill if still running
                        self.proc.kill()
            except:
                pass
            self.proc = None
            self.pid = None
    
    @gen.coroutine
    def poll(self):
        """Check if the single-user server is running"""
        if self.proc:
            return self.proc.poll()
        return 1  # Not running

c.JupyterHub.spawner_class = WorkingSpawner

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Admin users
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

# Create runtime directories
import os
os.makedirs('/workspace/jupyterhub/runtime', exist_ok=True)
os.makedirs('/workspace/jupyterhub/data', exist_ok=True)

print("JupyterHub working configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Authentication: DummyAuthenticator (any username, no password)")
print("Spawner: WorkingSpawner (custom implementation)")
print("This spawner directly runs Jupyter Lab for each user")